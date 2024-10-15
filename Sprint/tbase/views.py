from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Coords, Level, Images, PerevalAdded
from .serializers import UserSerializer, CoordsSerializer, LevelSerializer, ImagesSerializer, PerevalAddedSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalAddedViewSet(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    @action(detail=True, methods=['get'])
    def retrieve_perevaladded_object(self, request):
        id = request.query_params.get('id')
        if id:
            try:
                perevaladded_item = PerevalAdded.objects.get(id=id)
                serializer = PerevalAddedSerializer(perevaladded_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PerevalAdded.DoesNotExist:
                return Response({"message": "PerevalAddedItem not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please provide an id"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'patch'])
    def submitDataUpdate(self, request, **kwargs):
        id = kwargs.get('id')
        if id:
            try:
                instance = PerevalAdded.objects.get(id=id)
                if request.method == 'GET':
                    serializer = PerevalAddedSerializer(instance, context={'request': request})
                    return Response(serializer.data)
                elif request.method == 'PATCH':
                    serializer = PerevalAddedSerializer(instance, data=request.data, partial=True,
                                                        context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status": status.HTTP_200_OK, "message": "Объект успешно обновлен"})
                    else:
                        return Response({"status": status.HTTP_400_BAD_REQUEST, "message": serializer.errors})
            except PerevalAdded.DoesNotExist:
                return Response({"status": status.HTTP_404_NOT_FOUND, "message": "Объект не найден"})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "Не указан 'id' в параметрах запроса"})

    @action(detail=False, methods=['get'])
    def submitDataByEmail(self, request, email=None):
        if email:
            perevaladded_items = PerevalAdded.objects.filter(user__email=email)
            serializer = PerevalAddedSerializer(perevaladded_items, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Введите email пользователя в URL"}, status=status.HTTP_400_BAD_REQUEST)

    # ОПРЕДЕЛЯЕМ МЕТОД SubmitData ВНУТРИ КОНТРОЛЛЕРА
    # Извлечение данных, создание экземпляров соответствующих моделей, сохранение экземпляра PerevalAdded со связанными моделями
    @action(detail=False, methods=['post'])  # метод submitData является действием (action) для контроллера
    def submitData(self, request, status=None):
        data = request.data
        serializer = PerevalAddedSerializer(data=data)

        if serializer.is_valid():
            user_data = data.get('user')
            user_instance = User.objects.create(**user_data)
            coords_data = data.get('coords')
            coords_instance = Coords.objects.create(**coords_data)
            level_data = data.get('level')
            level_instance = Level.objects.create(**level_data)

            images_data = data.get('images')
            images_instances = [Images.objects.create(data=image.get('data'), title=image.get('title')) for image in
                                images_data]

            pereval_added = serializer.save(user=user_instance, coords=coords_instance, level=level_instance,
                                            images=images_instances)

            status = 'new'


            return Response({"status": status.HTTP_200_OK, "message": "Отправлено успешно", "id": pereval_added.id})
        else:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "Bad Request (при нехватке полей)", "id": None})
