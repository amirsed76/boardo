from django.shortcuts import render

from rest_framework import permissions
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from . import serializers, models
from django.http import Http404, HttpResponse
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from . import functions
from rest_framework.views import APIView
from django.shortcuts import redirect


# Create your views here.
def room(request, room_name):
    return render(request, 'catann/room.html', {
        'room_name': room_name
    })


class CatanEventCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.CatanEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.CatanEvent.objects.all()


class LoginGameAPIView(generics.CreateAPIView):
    serializer_class = serializers.PlayerGameSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.PlayerGame.objects.all()

    def validate(self, catan_event):
        if models.PlayerGame.objects.filter(player=self.request.user,
                                            catan_event=catan_event).exists():
            return Response({"value": "you are currently login"}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.data["password"] != catan_event.event.password:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if models.PlayerGame.objects.filter(catan_event=catan_event).count() > 4:
            return Response({"value": "capacity is full"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def start_game(room_name, catan_event):
        functions.send_message(message="game_started", room_name=room_name)
        player1 = models.PlayerGame.objects.filter(catan_event=catan_event)[0].player

        serializers.CatanEventSerializer().update(
            instance=models.CatanEvent.objects.get(event__room_name=room_name),
            validated_data={"state": "init1",
                            "turn": player1})

        functions.send_message(message={"turn": player1.id, "action": "init1"}, room_name=room_name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # print("okkkk")
            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            result_validate = self.validate(catan_event=catan_event)
            if result_validate is not None:
                return result_validate
            serializer.save(player=self.request.user, catan_event=catan_event)

            functions.send_message(message="one player added", room_name=kwargs["room_name"])

            if models.PlayerGame.objects.filter(catan_event=catan_event).count() == 4:
                catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
                self.start_game(room_name=kwargs["room_name"], catan_event=catan_event)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)


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


class Init1APIView(generics.CreateAPIView):
    serializer_class = serializers.Init1ActionSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO permission for init1

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        player_game = models.PlayerGame.objects.get(catan_event=catan_event, player=self.request.user)
        serializer.save(room_name=kwargs["room_name"], player_game=player_game)
        functions.send_message(message={"action": "init1", "args": serializer.data}, room_name=kwargs["room_name"])
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Init2APIView(generics.CreateAPIView):
    serializer_class = serializers.Init2ActionSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO permission for init2

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        player_game = models.PlayerGame.objects.get(catan_event=catan_event, player=self.request.user)
        serializer.save(room_name=kwargs["room_name"], player_game=player_game)
        functions.send_message(message={"action": "init2", "args": serializer.data}, room_name=kwargs["room_name"])
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PlayYearOfPlenty(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for year of plenty
    serializer_class = serializers.YearOfPlentySerializer

    def post(self, request, *args, **kwargs):
        player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                    catan_event__event__room_name=kwargs["room_name"])
        serializer = self.serializer_class(instance=player_game, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        functions.send_message(
            message={"action": "play_year_of_plenty",
                     "args": {"resource1": request.data["resource1"], "resource2": request.data["resource2"]}},
            room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayRoadBuilding(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for year of plenty
    serializer_class = serializers.RoadBuildingSerializer

    def post(self, request, *args, **kwargs):
        player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                    catan_event__event__room_name=kwargs["room_name"])
        serializer = self.serializer_class(instance=None, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save(player_game=player_game)

        data = request.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "play_road_building",
                     "args": data},
            room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response([], status=status.HTTP_200_OK)


class PlayMonopoly(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for monopoly
    serializer_class = serializers.MonopolySerializer

    def post(self, request, *args, **kwargs):
        player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                    catan_event__event__room_name=kwargs["room_name"])
        serializer = self.serializer_class(instance=player_game, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = request.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "monopoly",
                     "args": data},
            room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayKnightCard(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for knight+
    serializer_class = serializers.KnightSerializer

    def post(self, request, *args, **kwargs):
        player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                    catan_event__event__room_name=kwargs["room_name"])
        serializer = self.serializer_class(instance=player_game, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = request.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "knight",
                     "args": data},
            room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class DiceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for dice
    serializer_class = serializers.DiceSerializer

    def post(self, request, *args, **kwargs):
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        functions.send_message(room_name=kwargs["room_name"], message={
            "action": "dice", "args": {"dice1": dice1, "dice2": dice2}
        })
        # TODO send each player allocated resources
        if dice1 + dice2 != 7:
            tiles = models.Tile.objects.filter(number=dice1 + dice2)
            for tile in tiles:
                functions.allocate_resource(tile=tile)

            functions.send_message(room_name=kwargs["room_name"], message={
                "action": "dice", "args": {"dice1": dice1, "dice2": dice2}
            })
            catan_event.state = "trade_buy_build"
            catan_event.save()
            # functions.send_message(room_name=kwargs["room_name"],)
            # TODO send to all state

        else:
            functions.robbed(catan_event=catan_event)
            functions.send_message(room_name=kwargs["room_name"], message={
                "action": "dice", "args": {"dice1": dice1, "dice2": dice2}
            })
            # TODO send players each player one how many card robbed
            catan_event.state = "thief_tile"
            catan_event.save()
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response({"dice1": dice1, "dice2": dice2}, status=200)


class HomeCreateAPIView(generics.CreateAPIView):
    permission_classes = []  # TODO permission for create home
    queryset = models.Settlement.objects.all()
    serializers_class = serializers.HomeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player_game = models.PlayerGame.objects.get(catan_event__event__room_name=kwargs["room_name"],
                                                    player=self.request.user)
        serializer.save(kind="home", player_game=player_game)
        # TODO is finish ?
        functions.pay_resources_for_buy(salable="home", player_game=player_game)
        functions.send_message(room_name=kwargs["room_name"], message={"action": "build_home", "args": serializer.data})
        headers = self.get_success_headers(serializer.data)
        functions.send_message_status(catan_event=player_game.catan_event, room_name=kwargs["room_name"])

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CityUpdateAPIView(generics.UpdateAPIView):
    permission_classes = []  # TODO permission for create home
    queryset = models.Settlement.objects.all()
    serializers_class = serializers.CitySerializer

    def perform_update(self, serializer):
        serializer.save(kind="city")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        player_game = models.PlayerGame.objects.get(player=self.request.user, catan_event=catan_event)
        functions.pay_resources_for_buy(salable="city", player_game=player_game)
        # TODO is_finish
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RoadCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.RoadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        player_game = models.PlayerGame.objects.get(player=self.request.user, catan_event=catan_event)
        serializer.save(player_game=player_game)
        functions.pay_resources_for_buy(salable="road", player_game=player_game)
        functions.send_message(room_name=kwargs["room_name"], message={
            "action": "build_road",
            "args": serializer.data
        })

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BuyDevelopmentCard(APIView):
    serializer_class = serializers.BuyDevelopmentCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                    catan_event__event__room_name=kwargs["room_name"])
        serializer = self.serializer_class(instance=player_game, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        functions.send_message(
            message={"action": "buy_development_card",
                     "args": {}},
            room_name=kwargs["room_name"])
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        # TODO check finish
        return Response(serializer.data, status=status.HTTP_200_OK)
