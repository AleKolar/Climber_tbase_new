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
    add_time = serializers.DateTimeField()  # Handle add_time directly as a DateTimeField

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        add_time = validated_data.pop('add_time')  # Retrieve add_time directly as a DateTime value
        validated_data['add_time'] = add_time

        user_instance = User.objects.create(**user_data)
        coords_instance = Coords.objects.create(**coords_data)
        level_instance = Level.objects.create(**level_data)
        images_instances = [Images.objects.create(**image_data) for image_data in images_data]

        validated_data['user'] = user_instance
        validated_data['coords'] = coords_instance
        validated_data['level'] = level_instance
        validated_data['images'] = images_instances

        # Construct a dictionary representation of PerevalAdded object
        pereval_dict = {
            'beauty_title': validated_data.get('beauty_title'),
            'title': validated_data.get('title'),
            'other_titles': validated_data.get('other_titles'),
            'connect': validated_data.get('connect'),
            'add_time': add_time,
            'user': user_data,
            'coords': coords_data,
            'level': level_data,
            'images': images_data
        }

        # You can now use pereval_dict as needed before saving PerevalAdded object

        return PerevalAdded.objects.create(**validated_data)


