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

    # ОПРЕДЕЛЯЕМ МЕТОД SubmitData ВНУТРИ КОНТРОЛЛЕРА
    # Извлечение данных, создание экземпляров соответствующих моделей, сохранение экземпляра PerevalAdded со связанными моделями
    @action(detail=False, methods=['post'])  # метод submitData является действием (action) для контроллера
    def submitData(self, request):
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

            return Response({"status": status.HTTP_200_OK, "message": "Отправлено успешно", "id": pereval_added.id})
        else:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "Bad Request (при нехватке полей)", "id": None})


