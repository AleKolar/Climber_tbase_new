from rest_framework import serializers
from .models import User, Coord, Level, PerevalAdded, Images


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
    level = LevelSerializer()
    images = ImagesSerializer(many=True)  # Добавлено для сериализации связанных изображений

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')  # Добавлено для обработки изображений

        user_instance, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)
        coords_instance, created = Coord.objects.get_or_create(latitude=coords_data['latitude'],
                                                               longitude=coords_data['longitude'],
                                                               height=coords_data['height'])
        level_instance, created = Level.objects.get_or_create(winter=level_data['winter'], summer=level_data['summer'],
                                                              autumn=level_data['autumn'], spring=level_data['spring'])

        # Создание экземпляра PerevalAdded
        instance = PerevalAdded.objects.create(user=user_instance, coords=coords_instance, level=level_instance,
                                               **validated_data)

        # Обработка изображений
        for image_data in images_data:
            image_instance = Images.objects.create(**image_data)
            instance.images.add(image_instance)

        return instance