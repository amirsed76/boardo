from . import models
from rest_framework import serializers
import board_game_site.serializers  as board_game_serializers
import board_game_site.models  as board_game_models
import random
import registry.models as registry_models
from . import functions


class CatanEventSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(read_only=True, source="event.room_name")
    password = serializers.CharField(read_only=True, source="event.password")
    room_name = serializers.CharField(read_only=True, source="event.room_name")

    class Meta:
        model = models.CatanEvent
        fields = "__all__"
        read_only_fields = ["event", "turn", "state"]

    def create(self, validated_data):
        game = board_game_models.Game.objects.get(slug="catan")
        board_game_game_event_validate_data = {
            "game": game,
            "password": functions.get_random_string()
        }

        event = board_game_serializers.GameEventSerializer().create(board_game_game_event_validate_data)
        catan_event_validate_data = validated_data.copy()
        catan_event_validate_data["event"] = event
        instance = super(CatanEventSerializer, self).create(catan_event_validate_data)
        # initialize world
        functions.create_world(catan_event=instance)
        return instance

    def update_state(self, instance, state):
        instance=self.update(instance=instance, validated_data={"state": state})

    def update_turn(self, instance, user_id):
        user = registry_models.User.objects.get(pk=user_id)
        self.update(instance=instance, validated_data={"turn": user})


class PersonalSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    point = serializers.SerializerMethodField(read_only=True, method_name="get_point")
    player_avatar = serializers.ImageField(source="player.avatar.avatar", read_only=True)
    player_username = serializers.CharField(source="player.username", read_only=True)

    class Meta:
        model = models.PlayerGame
        fields = "__all__"
        read_only_fields = ["catan_event", "player", "brick_count", "sheep_count", "stone_count", "wheat_count",
                            "wood_count", "has_long_road_card", "has_largest_army", "monopoly_count", "year_of_plenty",
                            "road_building_count", "victory_point", "knight", "knight_card_played", "thief_tile"]

    @staticmethod
    def get_point(instance):
        point = 0
        if instance.has_largest_army:
            point += 2
        if instance.has_long_road_card:
            point += 2
        cities = models.Settlement.objects.filter(player_game=instance, kind="city")
        point += len(cities) * 2
        homes = models.Settlement.objects.filter(player_game=instance, kind="home")
        point += len(homes)
        point += instance.victory_point
        return point

    def save(self, **kwargs):
        user_game_serializer_validate_data = {"user": kwargs["player"], "game_event": kwargs["catan_event"].event,
                                              "is_winner": False}
        board_game_serializers.UserGameSerializer().create(user_game_serializer_validate_data)
        del self.validated_data["password"]
        return super(PersonalSerializer, self).save(**kwargs)


class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tile
        fields = "__all__"


class TileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tile
        fields = ["identify", "resource", "number"]


class PlayerInformationSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField("get_cards", read_only=True)
    resources = serializers.SerializerMethodField("get_resources", read_only=True)
    point = serializers.SerializerMethodField("get_point", read_only=True)
    road_length = serializers.SerializerMethodField("get_road_length", read_only=True)
    player_avatar = serializers.ImageField(source="player.avatar.avatar", read_only=True)
    player_username = serializers.CharField(source="player.username", read_only=True)

    class Meta:
        model = models.PlayerGame

        fields = ["id", "catan_event", "player", "has_long_road_card", "has_largest_army", "knight_card_played",
                  "cards", "resources", "point", "road_length", "player_avatar", "player_username"]

        read_only_fields = ["catan_event", "player", "has_long_road_card", "has_largest_army", "knight_card_played",
                            "cards", "resources", "point", "road_length"]

    @staticmethod
    def get_cards(instance):
        return instance.monopoly_count + instance.year_of_plenty + instance.road_building_count + instance.victory_point

    @staticmethod
    def get_resources(instance):
        return instance.brick_count + instance.sheep_count + instance.stone_count + \
               instance.wheat_count + instance.wood_count

    @staticmethod
    def get_point(instance):
        point = 0
        if instance.has_largest_army:
            point += 2
        if instance.has_long_road_card:
            point += 2
        cities = models.Settlement.objects.filter(player_game=instance, kind="city")
        point += len(cities) * 2
        homes = models.Settlement.objects.filter(player_game=instance, kind="home")
        point += len(homes)
        return point

    def get_road_length(self, instance):
        functions.get_longest_road(instance)
        return 0


class PlayerGameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayerGame
        fields = "__all__"


class Init1ActionSerializer(serializers.ModelSerializer):
    vertex = serializers.IntegerField()
    road_v1 = serializers.IntegerField()
    road_v2 = serializers.IntegerField()

    class Meta:
        model = models.Settlement
        fields = ["vertex", "road_v1", "road_v2"]

    def create(self, validated_data):
        home_instance = HomeSerializer().create(
            {"player_game": validated_data["player_game"], "vertex": validated_data["vertex"], "kind": "home"})

        RoadSerializer().create({"player_game": validated_data["player_game"], "vertex1": validated_data["road_v1"],
                                 "vertex2": validated_data["road_v2"]})
        if validated_data["player_game"] == models.PlayerGame.objects.filter(
                catan_event=validated_data["player_game"].catan_event).reverse()[0]:
            state = "init2"
            turn = validated_data["player_game"].player.id
        else:
            state = "init1"
            turn = validated_data["player_game"].next_player()

        CatanEventSerializer().update_state(instance=home_instance.player_game.catan_event, state=state)
        CatanEventSerializer().update_turn(instance=home_instance.player_game.catan_event, user_id=turn)

        return validated_data

    def validate(self, attrs):
        if attrs["vertex"] not in [attrs["road_v1"], attrs["road_v2"]]:
            raise serializers.ValidationError("home and road must be near together")
        # TODO road size must be one
        # TODO home and road with location not existed
        return attrs


class Init2ActionSerializer(serializers.ModelSerializer):
    vertex = serializers.IntegerField()
    road_v1 = serializers.IntegerField()
    road_v2 = serializers.IntegerField()

    class Meta:
        model = models.Settlement
        fields = ["vertex", "road_v1", "road_v2"]

    def create(self, validated_data):
        home_instance = HomeSerializer().create(
            {"player_game": validated_data["player_game"], "vertex": validated_data["vertex"], "kind": "home"})

        RoadSerializer().create({"player_game": validated_data["player_game"], "vertex1": validated_data["road_v1"],
                                 "vertex2": validated_data["road_v2"]})
        if validated_data["player_game"] == models.PlayerGame.objects.filter(
                catan_event=validated_data["player_game"].catan_event).reverse()[0]:
            state = "play_development_card"
            turn = validated_data["player_game"].player.id
        else:
            state = "init2"
            turn = validated_data["player_game"].next_player(reverse=True)

        CatanEventSerializer().update_state(instance=home_instance.player_game.catan_event, state=state)
        CatanEventSerializer().update_turn(instance=home_instance.player_game.catan_event, user_id=turn)

        player_game = home_instance.player_game
        tile_indexes = functions.vertex2tiles(vertex=validated_data["vertex"])

        Tile_validated_data = {"brick_count": player_game.brick_count,
                               "sheep_count": player_game.sheep_count,
                               "stone_count": player_game.stone_count,
                               "wheat_count": player_game.wheat_count,
                               "wood_count": player_game.wood_count}

        for tile_index in tile_indexes:
            tile = models.Tile.objects.get(identify=tile_index, catan_event=home_instance.player_game.catan_event)
            try:
                validated_data["{}_count".format(tile.resource)] += 1
            except:
                pass

        PlayerGameUpdateSerializer().update(instance=player_game,
                                            validated_data=Tile_validated_data)

        return validated_data

    def validate(self, attrs):
        if attrs["vertex"] not in [attrs["road_v1"], attrs["road_v2"]]:
            raise serializers.ValidationError("home and road must be near together")
        # TODO road size must be one
        # TODO home and road with location not existed
        return attrs


class YearOfPlentySerializer(serializers.Serializer):
    CHOICES = {("brick", "brick"),
               ("sheep", "sheep"),
               ("stone", "stone"),
               ("wheat", "wheat"),
               ("wood", "wood")}
    resource1 = serializers.ChoiceField(choices=CHOICES, write_only=True)
    resource2 = serializers.ChoiceField(choices=CHOICES, write_only=True)

    def update(self, instance, validated_data):
        for resource in [validated_data["resource1"], validated_data["resource2"]]:
            if resource == "brick":
                instance.brick_count += 1
            elif resource == "sheep":
                instance.sheep_count += 1

            elif resource == "stone":
                instance.stone_count += 1

            elif resource == "wheat":
                instance.wheat_count += 1

            elif resource == "wood":
                instance.wood_count += 1

        instance.year_of_plenty -= 1
        instance.save()

        instance.catan_event.state = "dice"
        instance.catan_event.save()

        return instance

    def create(self, validated_data):
        pass


class RoadBuildingSerializer(serializers.Serializer):
    road1_vertex1 = serializers.IntegerField(write_only=True)
    road1_vertex2 = serializers.IntegerField(write_only=True)
    road2_vertex1 = serializers.IntegerField(write_only=True)
    road2_vertex2 = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        road = models.Road(player_game=validated_data["player_game"], vertex1=validated_data["road1_vertex1"],
                           vertex2=validated_data["road1_vertex2"])
        road.save()

        road = models.Road(player_game=validated_data["player_game"], vertex1=validated_data["road2_vertex1"],
                           vertex2=validated_data["road2_vertex2"])
        road.save()

        validated_data["player_game"].road_building_count -= 1
        validated_data["player_game"].save()

        validated_data["player_game"].catan_event.state = "dice"
        validated_data["player_game"].catan_event.save()

        return validated_data["player_game"]

    def update(self, instance, validated_data):
        pass


class MonopolySerializer(serializers.Serializer):
    resource = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        resource = validated_data["resource"]
        players = models.PlayerGame.objects.filter(catan_event=instance.catan_event)
        count = 0
        for player in players:
            if player == instance:
                continue
            else:
                if resource == "brick":
                    count += player.brick_count
                    player.brick_count = 0

                elif resource == "sheep":
                    count += player.sheep_count
                    player.sheep_count = 0

                elif resource == "stone":
                    count += player.sheep_count
                    player.stone_count = 0

                elif resource == "wheat":
                    count += player.wheat_count
                    player.wheat_count = 0

                elif resource == "wood":
                    count += player.wood_count
                    player.wood_count = 0
            player.save()

        if resource == "brick":
            instance.brick_count += count

        elif resource == "sheep":
            instance.sheep_count += count

        elif resource == "stone":
            instance.stone_count += count

        elif resource == "wheat":
            instance.wheat_count += count

        elif resource == "wood":
            instance.wood_count += count

        instance.monopoly_count -= 1
        instance.save()

        instance.catan_event.state = "dice"
        instance.catan_event.save()

        return instance


class KnightSerializer(serializers.Serializer):
    tile = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.knight -= 1
        instance.knight_card_played += 1
        instance.save()
        # TODO get from a player a resource
        instance.catan_event.thief_tile = validated_data["tile"]
        instance.catan_event.state = "dice"
        instance.catan_event.save()

        return instance

    def create(self, validated_data):
        pass


class DiceSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settlement
        fields = ["vertex"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settlement
        fields = []


class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Road
        fields = "__all__"
        read_only_fields = ["player_game"]


class BuyDevelopmentCardSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        player_game = validated_data["player_game"]
        player_game: models.PlayerGame
        if functions.event_development_card_count(catan_event=player_game.catan_event) > 0:
            functions.pay_resources_for_buy(salable="development_card", player_game=validated_data["player_game"])
            card = functions \
                .pop_random_development_card(catan_event=instance.catan_event)
            return card
        else:
            raise Exception("all card is finish")

    def create(self, validated_data):
        pass


class GoodsSerializer(serializers.Serializer):
    brick = serializers.IntegerField()
    sheep = serializers.IntegerField()
    stone = serializers.IntegerField()
    wheat = serializers.IntegerField()
    wood = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TradeSerializer(serializers.Serializer):
    give = GoodsSerializer()
    want = GoodsSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        player_game = validated_data["player_game"]
        catan_event = player_game.catan_event
        catan_event.state = "answer_trade"
        catan_event.save()
        trade = models.Trade(player_game=player_game,
                             brick_want=validated_data["want"]["brick"],
                             sheep_want=validated_data["want"]["sheep"],
                             stone_want=validated_data["want"]["stone"],
                             wheat_want=validated_data["want"]["wheat"],
                             wood_want=validated_data["want"]["wood"],
                             brick_give=validated_data["give"]["brick"],
                             sheep_give=validated_data["give"]["sheep"],
                             stone_give=validated_data["give"]["stone"],
                             wheat_give=validated_data["give"]["wheat"],
                             wood_give=validated_data["give"]["wood"],
                             )
        trade.save()
        return trade


class AnswerTrade(serializers.ModelSerializer):
    class Meta:
        model = models.TradAnswer
        fields = ["answer", "id"]

    def create(self, validated_data):
        player_game = validated_data["player_game"]
        catan_event = player_game.catan_event
        catan_event.save()

        trad_answer = models.TradAnswer(
            trade=models.Trade.object.filter(player_game__catan_event=player_game.catan_event).order_by('-id')[0],
            player=player_game, answer=validated_data["answer"])
        trad_answer.save()
        return trad_answer


class TradAnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TradAnswer
        fields = "__all__"


class BankTradSerializer(serializers.Serializer):
    CHOICES = {("brick", "brick"),
               ("sheep", "sheep"),
               ("stone", "stone"),
               ("wheat", "wheat"),
               ("wood", "wood")}
    give = serializers.ChoiceField(choices=CHOICES, write_only=True)
    want = serializers.ChoiceField(choices=CHOICES, write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        player_game = validated_data["player_game"]
        catan_event = player_game.catan_event
        catan_event.state = "trade_buy_build"
        catan_event.save()
        if not functions.has_resource(player=player_game, resource=validated_data["give"], count=4):
            raise Exception("amount not enough")
        functions.change_player_resource(player=player_game, resource=validated_data["give"], count=-4)
        functions.change_player_resource(player=player_game, resource=validated_data["want"], count=1)
        return catan_event
