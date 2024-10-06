from rest_framework import serializers
from .models import User, Coords, Level, PerevalAdded, Images


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
        fields = '__all__'


def validate(self, data):
    user_data = data.get('user', None)
    user_email = user_data.get('email') if user_data else None

    if user_email:
        try:
            user = User.objects.get(email=user_email)
            # Если пользователь с таким email существует, можно просто использовать его
        except User.DoesNotExist:
            # Если пользователь с таким email не существует, создаем нового пользователя
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


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)
    add_time = serializers.DateTimeField()

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        add_time = validated_data.pop('add_time')
        validated_data['add_time'] = add_time

        pereval_added = PerevalAdded.objects.create(**validated_data)  # obj with unique ID

        # 'НАЗНАЧАЕМ' ВСЕМ ID ПЕРЕВАЛА
        user_instance = User.objects.create(id=pereval_added.id, **user_data)
        coords_instance = Coords.objects.create(id=pereval_added.id, **coords_data)
        level_instance = Level.objects.create(id=pereval_added.id, **level_data)
        images_instances = [Images.objects.create(id=pereval_added.id, **image_data) for image_data in images_data]

        pereval_added.user = user_instance
        pereval_added.coords = coords_instance
        pereval_added.level = level_instance
        pereval_added.save()

        pereval_added.images.set(images_instances)

        return pereval_added

