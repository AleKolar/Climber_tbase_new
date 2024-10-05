import logging

from rest_framework import serializers
from .models import User, Coord, Level, PerevalAdded, Images

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'level', 'status', 'user', 'coords',
                  'images']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        # Логирование информации в терминал
        logger.info("User Data: %s", user_data)
        logger.info("Coords Data: %s", coords_data)
        logger.info("Images Data: %s", images_data)

        user_instance = User.objects.create(**user_data)
        coords_instance = Coord.objects.create(**coords_data)

        images_instances = []
        for image_data in images_data:
            image = Images.objects.create(**image_data)
            images_instances.append(image)

        validated_data['user'] = user_instance
        validated_data['coords'] = coords_instance
        validated_data['images'] = images_instances

        return PerevalAdded.objects.create(**validated_data)
