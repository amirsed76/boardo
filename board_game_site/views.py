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
    permission_classes = []

    # def retrieve(self, request, *args, **kwargs):

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CommentSerializer
    queryset = models.GameComment.objects.filter(status="a")

    def create(self, request, *args, **kwargs):
        event = models.GameEvent.objects.get(room_name=kwargs["room_name"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_game=models.UserGame.objects.get(game_event=event, user=self.request.user))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class VoteCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.GameVote.objects.all()
    serializer_class = serializers.VoteSerializer

    def create(self, request, *args, **kwargs):
        event = models.GameEvent.objects.get(room_name=kwargs["room_name"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_game=models.UserGame.objects.get(game_event=event, user=self.request.user))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
