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
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images']

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

    # ИДЕНТИФИКАТОР ПОЛЬЗОВАТЕЛЯ _ ЭТО ЕГО EMAIL
    def validate(self, data):
        user_data = data.get('user', None)
        user_email = user_data.get('email') if user_data else None

        if user_email:
            try:
                user = User.objects.get(email=user_email)
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.save()
            except User.DoesNotExist:
                user_serializer = UserSerializer(data=user_data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                else:
                    raise serializers.ValidationError(user_serializer.errors)

        instance = self.instance
        if instance is not None:
            if instance.status != 'new':
                raise serializers.ValidationError(f'Отклонено! Статус {instance.get_status_display()}!')

        return data
