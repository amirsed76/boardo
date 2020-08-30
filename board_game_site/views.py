from rest_framework import permissions
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from . import serializers, models


class GameListAPIVies(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GameSerializer
    queryset = models.Game.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class GameRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.GameDetailSerializer
    queryset = models.Game.objects.all()
    permission_classes = [permissions.IsAuthenticated]

