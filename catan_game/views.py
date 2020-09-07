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
from . import permission


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
    serializer_class = serializers.PersonalSerializer
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
    permission_classes = [permissions.IsAuthenticated, permission.IsInCatanEvent]
    serializer_class = serializers.PersonalSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object(room_name=kwargs["room_name"])
            if instance is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return models.PlayerGame.objects.filter(player=self.request.user)

    def get_object(self, room_name):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(catan_event__event__room_name=room_name)
            self.check_object_permissions(self.request, obj)
        except:
            obj = None
        return obj

        # May raise a permission denied


class TileListAPIVIew(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TileListSerializer
    queryset = models.Tile.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = models.Tile.objects.filter(catan_event__event__room_name=kwargs["room_name"])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
        try:
            queryset = models.PlayerGame.objects.filter(catan_event__event__room_name=kwargs["room_name"])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class Init1APIView(generics.CreateAPIView):
    serializer_class = serializers.Init1ActionSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO permission for init1

    def initial(self, request, *args, **kwargs):
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        try:
            if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                                 obj=models.CatanEvent.objects.get(
                                                                     event__room_name=kwargs["room_name"])):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

        except Exception as e:
            print(e)
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )
        self.check_throttles(request)

    def create(self, request, *args, **kwargs):
        try:
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Init2APIView(generics.CreateAPIView):
    serializer_class = serializers.Init2ActionSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO permission for init2

    def initial(self, request, *args, **kwargs):
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        try:
            if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                                 obj=models.CatanEvent.objects.get(
                                                                     event__room_name=kwargs["room_name"])):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

        except:
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )
        self.check_throttles(request)

    def create(self, request, *args, **kwargs):
        try:
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PlayYearOfPlenty(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for year of plenty
    serializer_class = serializers.YearOfPlentySerializer

    def initial(self, request, *args, **kwargs):
        super(PlayYearOfPlenty, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        try:
            player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                        catan_event__event__room_name=kwargs["room_name"])
            player_game: models.PlayerGame

            if player_game.year_of_plenty < 1:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
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

    def initial(self, request, *args, **kwargs):
        super(PlayRoadBuilding, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):

        try:
            player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                        catan_event__event__room_name=kwargs["room_name"])
            player_game: models.PlayerGame

            if player_game.road_building_count < 1:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=None, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save(player_game=player_game)
        functions.update_longest_road(catan_event=catan_event)

        data = request.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "play_road_building",
                     "args": data},
            room_name=kwargs["room_name"])
        functions.check_finish(catan_event=catan_event)
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response([], status=status.HTTP_200_OK)


class PlayMonopoly(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for monopoly
    serializer_class = serializers.MonopolySerializer

    def initial(self, request, *args, **kwargs):
        super(PlayMonopoly, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        try:
            player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                        catan_event__event__room_name=kwargs["room_name"])
            player_game: models.PlayerGame

            if player_game.year_of_plenty < 1:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

    def initial(self, request, *args, **kwargs):
        super(PlayKnightCard, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        try:
            player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                        catan_event__event__room_name=kwargs["room_name"])
            player_game: models.PlayerGame

            if player_game.knight < 1:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=player_game, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        functions.update_largest_army(catan_event=catan_event)
        data = request.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "knight",
                     "args": data},
            room_name=kwargs["room_name"])
        functions.check_finish(catan_event=catan_event)
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class DiceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO  permission for dice
    serializer_class = serializers.DiceSerializer

    def initial(self, request, *args, **kwargs):
        super(DiceAPIView, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        try:
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
            # return Response( status=200)
            return Response({"dice1": dice1, "dice2": dice2}, status=200)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class HomeCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO permission for create home
    queryset = models.Settlement.objects.all()
    serializer_class = serializers.HomeSerializer

    def initial(self, request, *args, **kwargs):
        super(HomeCreateAPIView, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            player_game = models.PlayerGame.objects.get(catan_event=catan_event,
                                                        player=self.request.user)
            serializer.save(kind="home", player_game=player_game)
            functions.pay_resources_for_buy(salable="home", player_game=player_game)
            data = serializer.data.copy()
            del data["csrfmiddlewaretoken"]
            functions.send_message(room_name=kwargs["room_name"], message={"action": "build_home", "args": data})
            functions.check_finish(catan_event=catan_event)
            functions.send_message_status(catan_event=player_game.catan_event, room_name=kwargs["room_name"])
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CityUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # TODO permission for create home
    queryset = models.Settlement.objects.all()
    serializer_class = serializers.CitySerializer

    def initial(self, request, *args, **kwargs):
        super(CityUpdateAPIView, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def perform_update(self, serializer):
        serializer.save(kind="city")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            player_game = models.PlayerGame.objects.get(player=self.request.user, catan_event=catan_event)
            functions.pay_resources_for_buy(salable="city", player_game=player_game)
            data = serializer.data.copy()
            del data["csrfmiddlewaretoken"]
            functions.send_message(room_name=kwargs["room_name"],
                                   message={"action": "build_city", "args": serializer.data})
            functions.check_finish(catan_event=catan_event)
            functions.send_message_status(catan_event=player_game.catan_event, room_name=kwargs["room_name"])
        except:
            return Response(status=status)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RoadCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.RoadSerializer

    def initial(self, request, *args, **kwargs):
        super(RoadCreateAPIView, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            player_game = models.PlayerGame.objects.get(player=self.request.user, catan_event=catan_event)
            serializer.save(player_game=player_game)
            functions.update_longest_road(catan_event=catan_event)
            functions.pay_resources_for_buy(salable="road", player_game=player_game)
            data = serializer.data.copy()
            del data["csrfmiddlewaretoken"]
            functions.send_message(room_name=kwargs["room_name"], message={
                "action": "build_road",
                "args": data
            })
            functions.check_finish(catan_event=catan_event)
            functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BuyDevelopmentCard(APIView):
    serializer_class = serializers.BuyDevelopmentCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super(BuyDevelopmentCard, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                    catan_event__event__room_name=kwargs["room_name"])
        serializer = self.serializer_class(instance=player_game, data=request.data,
                                           partial=True)

        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "buy_development_card",
                     "args": data},
            room_name=kwargs["room_name"])
        functions.check_finish(catan_event=catan_event)
        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class TradAPIView(generics.CreateAPIView):
    serializer_class = serializers.TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        try:
            super(TradAPIView, self).initial(request, *args, **kwargs)
            if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                                 obj=models.CatanEvent.objects.get(
                                                                     event__room_name=kwargs["room_name"])):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            player_game = models.PlayerGame.objects.get(catan_event=catan_event, player=self.request.user)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(player_game=player_game)

            # data = request.data.copy()
            # try:
            #     del data["csrfmiddlewaretoken"]
            # except:
            #     pass
            # data["id"] = serializer["id"]
            functions.send_message(
                message={"action": "trade",
                         "args": request.data},

                room_name=kwargs["room_name"])

            functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            # raise e
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AnswerTradeCreateAPIView(generics.CreateAPIView):
    # serializer_class = serializers.Tra
    # TODO Permission
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(catan_event=catan_event)
        data = serializer.data.copy()
        del data["csrfmiddlewaretoken"]
        functions.send_message(
            message={"action": "trade_answer",
                     "args": data},

            room_name=kwargs["room_name"])

        functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AnswerListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TradAnswerListSerializer

    def get_queryset(self):
        models.TradAnswer.objects.all()

    def list(self, request, *args, **kwargs):
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        trade = models.Trade.objects.filter(player_game__catan_event=catan_event).order_by("-id")[0]
        queryset = models.TradAnswer.objects.filter(trade=trade)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AcceptRejectAnswerTrade(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        # trade_answer=


class BankTrade(APIView):
    serializer_class = serializers.TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super(BankTrade, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        try:
            player_game = models.PlayerGame.objects.get(player=self.request.user,
                                                        catan_event__event__room_name=kwargs["room_name"])
            serializer = self.serializer_class(data=request.data, partial=True)

            catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data.copy()
            del data["csrfmiddlewaretoken"]
            functions.send_message(
                message={"action": "trade_bank",
                         "args": data},
                room_name=kwargs["room_name"])
            functions.send_message_status(catan_event=catan_event, room_name=kwargs["room_name"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EndRound(APIView):
    def initial(self, request, *args, **kwargs):
        super(EndRound, self).initial(request, *args, **kwargs)
        if not permission.IsUserTurn().has_object_permission(request=request, view=self,
                                                             obj=models.CatanEvent.objects.get(
                                                                 event__room_name=kwargs["room_name"])):
            self.permission_denied(
                request, message=getattr(permission, 'message', None)
            )

    def post(self, request, *args, **kwargs):
        catan_event = models.CatanEvent.objects.get(event__room_name=kwargs["room_name"])
        player_game = models.PlayerGame.objects.get(catan_event=catan_event, player=self.request.user)
        catan_event.state = "play_development_card"
        catan_event.turn = player_game.next()
        catan_event.save()
        functions.send_message(room_name=kwargs["room_name"], message={"action": "end_round", "args": {}})
        functions.send_message_status(catan_event=catan_event)
        return Response(status=status.HTTP_200_OK)
