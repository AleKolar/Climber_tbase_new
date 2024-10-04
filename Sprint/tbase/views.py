import json
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, CoordsSerializer, PerevalAddedSerializer, PerevalImagesSerializer


class SubmitDataView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data.get('user'))
        coords_serializer = CoordsSerializer(data=request.data.get('coords'))
        pereval_data = request.data.copy()
        pereval_data['status'] = 'new'
        pereval_serializer = PerevalAddedSerializer(data=pereval_data)
        images_serializer = PerevalImagesSerializer(data=request.data.get('images'), many=True)

        if user_serializer.is_valid() and coords_serializer.is_valid() and pereval_serializer.is_valid() and images_serializer.is_valid():
            user_obj = user_serializer.save()
            coords_obj = coords_serializer.save()
            pereval_data['user'] = user_obj.id
            pereval_data['coords'] = coords_obj.id
            pereval_obj = pereval_serializer.create(pereval_data)
            pereval_obj.save()
            images_serializer.save()

            pereval_data_for_api = {
                "beauty_title": pereval_obj.beautyTitle,
                "title": pereval_obj.title,
                "other_titles": pereval_obj.other_titles,
            }

            external_api_url = 'http://some_kind_of_external_api_where_will_I_send_it_url/submitData/'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(external_api_url, data=json.dumps(pereval_data_for_api), headers=headers)

            # Проверка ответа от внешнего API URL
            if response.status_code == 200:
                return Response({'status': 200, 'message': 'Отправлено успешно и на внешний API', 'id': pereval_obj.id},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 400, 'message': 'Ошибка при отправке на внешний API', 'id': pereval_obj.id},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 400, 'message': 'Bad Request - Некорректные данные', 'id': None},
                            status=status.HTTP_400_BAD_REQUEST)
