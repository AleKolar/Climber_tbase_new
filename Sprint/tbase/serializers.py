from rest_framework import serializers
from .models import User, Coords, Level, Images, PerevalAdded


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title']


# СОЗДАЕМ ЭКЗЕМПЛЯР КЛАССА ИЗ СВЯЗАННЫХ МОДЕЛЕЙ
# !!! ХОРОШО БЫ ИСПОЛЬЗОВАТЬ : WritableNestedModelSerializer !!!
# drf_writable_nested.serializers НЕ СТАВИТЬСЯ , ХОТЬ СЕРТИФИКАТ СКАЧАН _ РАЗБИРАТЬСЯ, СЕЙЧАС НЕКОГДА !!!
class PerevalAddedSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = ['id', 'status', 'url','beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images']

    # Извлечение и удаление данных о пользователе из проверенных данных, чтобы корректно обработать,
    # связанные модели при создании нового экземпляра модели PerevalAdded
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user_instance, created = User.objects.get_or_create(**user_data)
        coords_instance = Coords.objects.create(**coords_data)
        level_instance = Level.objects.create(**level_data)
        pereval = PerevalAdded.objects.create(**validated_data, user=user_instance, coords=coords_instance,
                                              level=level_instance)

        images_instances = [Images.objects.create(pereval=pereval, **image_data) for image_data in images_data]

        pereval.images.set(images_instances)

        return pereval

    def update(self, instance, validated_data):
        # Обновление собственных полей сущности
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.status = validated_data.get('status', instance.status)

        # Обновление связанных полей level
        level_data = validated_data.get('level', {})
        instance.level.summer = level_data.get('summer', instance.level.summer)
        instance.level.autumn = level_data.get('autumn', instance.level.autumn)
        instance.level.winter = level_data.get('winter', instance.level.winter)
        instance.level.spring = level_data.get('spring', instance.level.spring)
        instance.level.save()

        # Обновление связанных полей coords
        coords_data = validated_data.get('coords', {})
        instance.coords.latitude = coords_data.get('latitude', instance.coords.latitude)
        instance.coords.longitude = coords_data.get('longitude', instance.coords.longitude)
        instance.coords.height = coords_data.get('height', instance.coords.height)
        instance.coords.save()

        # Обновление изображений
        images_data = validated_data.get('images', [])

        for image_data in images_data:
            image_id = image_data.get('id')

            if image_id:
                try:
                    # Попытка получить существующее изображение
                    image_instance = Images.objects.get(id=image_id)
                    image_instance.data = image_data.get('data', image_instance.data)
                    image_instance.title = image_data.get('title', image_instance.title)
                    image_instance.pereval_id = instance.id  # Устанавливаем pereval_id
                    image_instance.save()
                except Images.DoesNotExist:
                    # Если изображение не найдено, создадим новое
                    new_image_instance = Images.objects.create(data=image_data.get('data'),
                                                               title=image_data.get('title'), pereval_id=instance.id)
                    instance.images.add(new_image_instance)
            else:
                # Создание нового изображения
                new_image_instance = Images.objects.create(data=image_data.get('data'), title=image_data.get('title'),
                                                           pereval_id=instance.id)
                instance.images.add(new_image_instance)


        instance.save()
        return instance

    # Переопределяем валидацию для доп. проверки на неизменение данных пользователя
    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            user_data = data.get('user')
            validating_user_fields = [
                instance_user.email != user_data['email'],
                instance_user.phone != user_data['phone'],
                instance_user.fam != user_data['fam'],
                instance_user.name != user_data['name'],
                instance_user.otc != user_data['otc'],
            ]
            if user_data is not None and any(validating_user_fields):
                raise serializers.ValidationError('Данные пользователя не могут быть изменены')
        return data

    # ИДЕНТИФИКАТОР ПОЛЬЗОВАТЕЛЯ _ ЭТО ЕГО EMAIL
    # def validate(self, data):
    #     user_data = data.get('user', None)
    #     user_email = user_data.get('email') if user_data else None
    #
    #     if user_email:
    #         try:
    #             user = User.objects.get(email=user_email)
    #             for key, value in user_data.items():
    #                 setattr(user, key, value)
    #             user.save()
    #         except User.DoesNotExist:
    #             user_serializer = UserSerializer(data=user_data)
    #             if user_serializer.is_valid():
    #                 user = user_serializer.save()
    #             else:
    #                 raise serializers.ValidationError(user_serializer.errors)
    #
    #     instance = self.instance
    #     if instance is not None:
    #         if instance.status != 'new':
    #             raise serializers.ValidationError(f'Отклонено! Статус {instance.get_status_display()}!')
    #
    #     return data
