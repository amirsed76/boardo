from . import models
from rest_framework import serializers
import board_game_site.serializers  as board_game_serializers
import board_game_site.models  as board_game_models
import random


def create_world(catan_event):
    RESOURSESE = {
        ("brick", "brick"),  # 3
        ("sheep", "sheep"),  # 4
        ("stone", "stone"),  # 3
        ("wheat", "wheat"),  # 4
        ("wood", "wood"),  # 4
        ("desert", "desert")  # 1
    }
    resources = []
    for i in range(0, 3):
        resources.append("brick")
    for i in range(0, 4):
        resources.append("sheep")
    for i in range(0, 3):
        resources.append("stone")
    for i in range(0, 3):
        resources.append("stone")
    for i in range(0, 4):
        resources.append("wheat")
    for i in range(0, 4):
        resources.append("wood")
    resources.append("desert")
    random.shuffle(resources)
    numbers = shuffle_numbers()
    j = 0
    for i in range(1, 20):
        resource = resources[i - 1]
        number = j
        if resource == "desert":
            number = 7
        else:
            j += 1
        TileSerializer().create(
            validated_data={"catan_event": catan_event, "identify": i, "resource": resource,
                            "number": number})


def shuffle_numbers():
    t1 = [2, 4, 5]
    t2 = [1, 3, 5, 6]
    t3 = [2, 6, 7]
    t4 = [1, 5, 8, 9]
    t5 = [1, 2, 4, 6, 9, 10]
    t6 = [2, 3, 5, 7, 10, 11]
    t7 = [3, 6, 11, 12]
    t8 = [4, 9, 13]
    t9 = [4, 5, 8, 10, 13, 14]
    t10 = [5, 6, 9, 11, 14, 15]
    t11 = [6, 7, 10, 12, 15, 16]
    t12 = [7, 11, 16]
    t13 = [8, 9, 14, 17]
    t14 = [9, 10, 13, 15, 17, 18]
    t15 = [10, 11, 14, 16, 18, 19]
    t16 = [11, 12, 15, 19]
    t17 = [13, 14, 18]
    t18 = [14, 15, 17, 19]
    t19 = [15, 16, 18]
    tiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19]
    result = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12, 7]

    # TODO write shuffle
    return [10, 2, 9, 12, 6, 14, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]


class CatanEventSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    room_name = serializers.CharField(read_only=True, source="event.room_name")

    class Meta:
        model = models.CatanEvent
        fields = "__all__"
        read_only_fields = ["event", "turn", "state"]

    def create(self, validated_data):
        game = board_game_models.Game.objects.get(slug="catan")
        board_game_game_event_validate_data = {
            "game": game,
            "password": validated_data["password"]
        }

        event = board_game_serializers.GameEventSerializer().create(board_game_game_event_validate_data)
        catan_event_validate_data = validated_data.copy()
        del catan_event_validate_data["password"]
        catan_event_validate_data["event"] = event
        instance = super(CatanEventSerializer, self).create(catan_event_validate_data)
        # initialize world
        create_world(catan_event=instance)
        return instance


class PlayerGameSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    point = serializers.SerializerMethodField(read_only=True, method_name="get_point")

    class Meta:
        model = models.PlayerGame
        fields = "__all__"
        read_only_fields = ["catan_event", "player", "brick_count", "sheep_count", "stone_count", "wheat_count",
                            "wood_count", "has_long_road_card", "has_largest_army", "monopoly_count", "year_of_plenty",
                            "road_building_count", "victory_point", "knight", "knight_card_played"]

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
        return super(PlayerGameSerializer, self).save(**kwargs)


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

    class Meta:
        model = models.PlayerGame
        fields = ["catan_event", "player", "has_long_road_card", "has_largest_army", "knight_card_played",
                  "cards", "resources", "point", "road_length"]
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
        # TODO write function
        return 0


class PlayerGameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayerGame
        fields = "__all__"


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settlement
        fields = ["vertex"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Settlement
        fields = []
