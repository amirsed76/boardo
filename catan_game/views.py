from django.shortcuts import render

from rest_framework import permissions
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from . import serializers, models
from django.http import Http404
import random


# Create your views here.
def room(request, room_name):
    return render(request, 'catann/room.html', {
        'room_name': room_name
    })


class CatanEventCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.CatanEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.CatanEvent.objects.all()


# models.PlayerGame

class PlayerGameCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PlayerGameSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.PlayerGame.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if models.PlayerGame.objects.filter(player=self.request.user,
                                                catan_event__event__room_name=kwargs["room_name"]).exists():
                return Response({"value": "you are currently login"})
            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            if self.request.data["password"] != catan_event.event.password:
                return Response(status=status.HTTP_403_FORBIDDEN)

            if models.PlayerGame.objects.filter(catan_event=catan_event).count() > 4:
                return Response({"value": "capacity is full"})

            self.perform_create(serializer, catan_event)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            print("xxxxxx", e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer, catan_event):
        serializer.save(player=self.request.user, catan_event=catan_event)


class PersonalInformation(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.PlayerGameSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(room_name=kwargs["room_name"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        return models.PlayerGame.objects.filter(player=self.request.user)

    def get_object(self, room_name):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(catan_event__event__is_active=True,
                               catan_event__event__room_name=room_name)
        except:
            obj = Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class TileListAPIVIew(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TileListSerializer
    queryset = models.Tile.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = models.Tile.objects.filter(catan_event__event__room_name=kwargs["room_name"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PlayerInformationListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.PlayerInformationSerializer
    queryset = models.PlayerGame.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = models.PlayerGame.objects.filter(catan_event__event__room_name=kwargs["room_name"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DiceAPIView(generics.GenericAPIView):
    def post(self, *args, **kwargs):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        # TODO allocate resorces
        return Response({"dice1": dice1, "dice2": dice2})


class HomeCreateAPIView(generics.CreateAPIView):
    permission_classes = []  # TODO permission for create home
    queryset = models.Settlement.objects.all()
    serializers_class = serializers.HomeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, kwargs["room_name"])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, room_name):
        try:
            serializer.save(kind="home",
                            player_game=models.PlayerGame.objects.get(catan_event__event__room_name=room_name,
                                                                      player=self.request.user))
        except:
            pass


class CityUpdateAPIView(generics.UpdateAPIView):
    permission_classes = []  # TODO permission for create home
    queryset = models.Settlement.objects.all()
    serializers_class = serializers.CitySerializer

    def perform_update(self, serializer):
        serializer.save(kind="city")

# class BuyDevelopmentCardCreate
