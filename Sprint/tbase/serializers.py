from rest_framework import serializers
from datetime import datetime

from .models import User, Coord, PerevalAdded, PerevalImages, Level

LEVEL_CHOICES = (
    ('1A', '1A'),
    ('1B', '1B'),
    ('2A', '2A'),
    ('2B', '2B'),
    ('3A', '3A'),
    ('3B', '3B'),
)


class LevelSerializer(serializers.Serializer):
    winter = serializers.ChoiceField(choices=LEVEL_CHOICES, allow_blank=True)
    summer = serializers.ChoiceField(choices=LEVEL_CHOICES, allow_blank=True)
    autumn = serializers.ChoiceField(choices=LEVEL_CHOICES, allow_blank=True)
    spring = serializers.ChoiceField(choices=LEVEL_CHOICES, allow_blank=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = '__all__'


class PerevalAddedSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='new')
    level = LevelSerializer()

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    def to_internal_value(self, data):
        if 'add_time' in data:
            data['add_time'] = datetime.strptime(data['add_time'], '%Y-%m-%d %H:%M:%S')
        return super(PerevalAddedSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        level_data = validated_data.pop('level')  # Извлекаем данные уровня сложности
        user_data = validated_data.pop('user')  # Извлекаем данные пользователя
        coord_data = validated_data.pop('coords')  # Извлекаем данные координат

        user_instance = User.objects.create(**user_data)  # Создаем объект User
        coord_instance = Coord.objects.create(**coord_data)  # Создаем объект Coord
        level_instance = Level.objects.create(**level_data)  # Создаем объект Level

        validated_data['user'] = user_instance  # Устанавливаем связь с объектом User
        validated_data['coords'] = coord_instance  # Устанавливаем связь с объектом Coord
        validated_data['level'] = level_instance  # Устанавливаем связь с объектом Level

        validated_data['status'] = 'new'
        return PerevalAdded.objects.create(**validated_data)


class PerevalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImages
        fields = '__all__'
