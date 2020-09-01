from . import models
from . import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, viewsets
import random


# generics.ListAPIView.list()

def send_message(message, room_name):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(room_name, {
        'type': 'chat_message',
        'message': message
    })


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


def get_random_string(length=5):
    # put your letters in the following string
    sample_letters = '1234567890'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


def get_tiles():
    tile = [[] for i in range(0, 20)]
    tile[1] = [1, 4, 5, 8, 9, 13]
    tile[2] = [2, 5, 6, 9, 10, 14]
    tile[3] = [3, 6, 7, 10, 11, 15]
    tile[4] = [8, 12, 13, 17, 18, 23]
    tile[5] = [9, 13, 14, 18, 19, 24]
    tile[6] = [10, 14, 15, 19, 20, 25]
    tile[7] = [11, 15, 16, 20, 21, 26]
    tile[8] = [17, 22, 23, 28, 29, 34]
    tile[9] = [18, 23, 24, 29, 30, 35]
    tile[10] = [19, 24, 25, 30, 31, 36]
    tile[11] = [20, 25, 26, 31, 32, 37]
    tile[12] = [21, 26, 27, 32, 33, 38]
    tile[13] = [29, 34, 35, 39, 40, 44]
    tile[14] = [30, 35, 36, 40, 41, 45]
    tile[15] = [31, 36, 37, 41, 42, 46]
    tile[16] = [32, 37, 38, 42, 43, 47]
    tile[17] = [40, 44, 45, 48, 49, 52]
    tile[18] = [41, 45, 46, 49, 50, 53]
    tile[19] = [42, 46, 47, 50, 51, 54]

    return tile


def finish_game(catan_event):
    queryset = models.PlayerGame.objects.filter(catan_event=catan_event)
    for instance in queryset:
        serializer = serializers.PlayerGameSerializer(instance=instance)
        if serializer.data["point"] >= 10:
            return instance

    return None


def allocate_resources(number, catan_event):
    tiles = models.Tile.objects.filter(catan_event=catan_event, number=number)
    tile = get_tiles()
    for t in tiles:
        for vertex in tile[t.identify]:
            try:
                settlement = models.Settlement.objects.get(vertex=vertex)
                # serializers.PlayerGameUpdateSerializer().update(instance=settlement.player_game )
                # settlement.player_game
                if settlement.kind == "home":
                    pass
                elif settlement.kind == "city":
                    pass

            except:
                pass


def vertex2tiles(vertex):
    tiles_neighbours = get_tiles()
    result = []
    for index, tile_neighbours in enumerate(tiles_neighbours):
        if vertex in tile_neighbours:
            result.append(index)

    return result


def tile2vertexes(tile_index):
    return get_tiles()[tile_index]


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
        serializers.TileSerializer().create(
            validated_data={"catan_event": catan_event, "identify": i, "resource": resource,
                            "number": number})

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
