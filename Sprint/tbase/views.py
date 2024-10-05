from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, CoordSerializer, PerevalAddedSerializer, PerevalImagesSerializer
import requests
import json


class SubmitDataView(APIView):
    def post(self, request):
        user_data = request.data.get('user')
        coords_data = request.data.get('coords')
        images_data = request.data.get('images')

        user_serializer = UserSerializer(data=user_data)
        coords_serializer = CoordSerializer(data=coords_data)
        pereval_data = {
            'beauty_title': request.data.get('beauty_title'),
            'title': request.data.get('title'),
            'other_titles': request.data.get('other_titles'),
            'connect': request.data.get('connect'),
            'add_time': request.data.get('add_time'),
            'level': {
                'winter': request.data.get('level').get('winter'),
                'summer': request.data.get('level').get('summer'),
                'autumn': request.data.get('level').get('autumn'),
                'spring': request.data.get('level').get('spring'),
            },
            'status': 'new',
        }

        pereval_serializer = PerevalAddedSerializer(data=pereval_data)
        images_serializer = PerevalImagesSerializer(data=images_data, many=True)

        if user_serializer.is_valid() and coords_serializer.is_valid() and pereval_serializer.is_valid() and images_serializer.is_valid():
            user_obj = user_serializer.save()
            coords_obj = coords_serializer.save()
            pereval_data['user'] = user_obj.id
            pereval_data['coords'] = coords_obj.id
            pereval_obj = pereval_serializer.create(pereval_data)
            pereval_obj.save()
            images_serializer.save()

            pereval_data_for_api = {
                "beauty_title": pereval_obj.beauty_title,
                "title": pereval_obj.title,
                "other_titles": pereval_obj.other_titles,
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
