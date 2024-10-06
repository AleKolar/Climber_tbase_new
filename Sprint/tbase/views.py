from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json

from .models import Images, Coords, User, Level
from .serializers import PerevalAddedSerializer


class SubmitDataView(APIView):
    def post(self, request):
        # Создание объекта User
        user_data = request.data.get('user')
        user_email = user_data.get('email')
        user_instance, created = User.objects.get_or_create(email=user_email, defaults=user_data)

        # Создание объекта Coords
        coords_data = request.data.get('coords')
        coords_instance = Coords.objects.create(**coords_data)
        coords_instance.save()

        # Создание объектов Images
        images_data = request.data.get('images')
        images_instances = [Images.objects.create(**image) for image in images_data]
        for image_instance in images_instances:
            image_instance.save()

        # Создание объектов Level
        level_data = request.data.get('level')
        level_instance = Level.objects.create(**level_data)

        # Создание объекта PerevalAdded с использованием email от User
        pereval_data = request.data
        pereval_data['user'] = user_email
        pereval_data['coords'] = coords_instance.pk

        pereval_serializer = PerevalAddedSerializer(data=pereval_data)

        if pereval_serializer.is_valid():
            pereval_obj = pereval_serializer.save()

            pereval_obj.images.set(images_instances)

            pereval_data_for_api = {
                "beauty_title": pereval_obj.beauty_title,
                "title": pereval_obj.title,
                "other_titles": pereval_obj.other_titles,
                "images": [image.data for image in pereval_obj.images.all()],
            }

            external_api_url = 'http://example.com/api/submit/'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(external_api_url, data=json.dumps(pereval_data_for_api), headers=headers)

            if response.status_code == 200:
                return Response({'status': 200, 'message': 'Отправлено успешно и на внешний API', 'id': pereval_obj.id},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 400, 'message': 'Ошибка при отправке на внешний API', 'id': pereval_obj.id},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 400, 'message': 'Bad Request - Некорректные данные', 'id': None},
                            status=status.HTTP_400_BAD_REQUEST)




