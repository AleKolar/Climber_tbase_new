from .serializers import PerevalAddedSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json


class SubmitDataView(APIView):
    def post(self, request):
        pereval_serializer = PerevalAddedSerializer(data=request.data)

        if pereval_serializer.is_valid():
            pereval_obj = pereval_serializer.save()

            # Отправка данных на внешний API - это мне надо !!!
            pereval_data_for_api = {
                "beauty_title": pereval_obj.beauty_title,
                "title": pereval_obj.title,
                "other_titles": pereval_obj.other_titles,
                "images": [image.data for image in pereval_obj.images.all()],
                # Включение данных изображений для отправки
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


