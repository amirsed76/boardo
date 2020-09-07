from . import models
from . import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, viewsets
import random
import networkx as nx


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
    # return [10, 2, 9, 12, 6, 14, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]
    return [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]


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
        serializer = serializers.PersonalSerializer(instance=instance)
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
        number = numbers[j]
        if resource == "desert":
            number = 7
            catan_event.thief_tile = i

        else:
            j += 1
        serializers.TileSerializer().create(
            validated_data={"catan_event": catan_event, "identify": i, "resource": resource,
                            "number": number})
    catan_event.save()


def get_point(player_game):
    point = 0
    if player_game.has_largest_army:
        point += 2
    if player_game.has_long_road_card:
        point += 2
    cities = models.Settlement.objects.filter(player_game=player_game, kind="city")
    point += len(cities) * 2
    homes = models.Settlement.objects.filter(player_game=player_game, kind="home")
    point += len(homes)
    return point


def change_player_resource(player, resource, count, save=True):
    if resource == "brick":
        player.brick_count += count

    elif resource == "sheep":
        player.sheep_count += count

    elif resource == "stone":
        player.stone_count += count

    elif resource == "wheat":
        player.wheat_count += count

    elif resource == "wood":
        player.wood_count += count

    if save:
        player.save()


def allocate_resource(tile):
    settlements = models.Settlement.objects.filter(vertex__in=tile2vertexes(tile_index=tile.identify),
                                                   player_game__catan_event=tile.catan_event)
    for settlement in settlements:
        if settlement.kind == "home":
            change_player_resource(player=settlement.player_game, resource=tile.resource, count=1)

        if settlement.kind == "city":
            change_player_resource(player=settlement.player_game, resource=tile.resource, count=2)


def robbed(catan_event):
    players = models.PlayerGame.objects.filter(catan_event=catan_event)

    for player in players:
        stone_count = player.stone_count
        wood_count = player.wood_count
        wheat_count = player.wheat_count
        sheep_count = player.sheep_count
        brick_count = player.brick_count
        cards_count = stone_count + sheep_count + wood_count + wheat_count + brick_count
        cards = ["stone" for s in range(stone_count)]
        cards.extend(["wood" for w in range(wood_count)])
        cards.extend(["wheat" for w in range(wheat_count)])
        cards.extend(["sheep" for s in range(sheep_count)])
        cards.extend(["brick" for b in range(brick_count)])
        if cards_count > 7:
            random.shuffle(cards)
            for card in cards[0:len(cards) / 2]:
                change_player_resource(player=player, resource=card, count=-1, save=False)

        player.save()


def get_need_resources(salable: str):
    if salable == "home":
        return ["wheat", "wood", "sheep", "brick"]

    if salable == "city":
        return ["stone", "stone", "stone", "wheat", "wheat"]

    if salable == "road":
        return ["wood", "brick"]

    if salable == "development_card":
        return ["stone", "sheep", "wheat"]


def pay_resources_for_buy(salable, player_game):
    needed_resources = get_need_resources(salable=salable)
    for resource in needed_resources:
        change_player_resource(player=player_game, resource=resource, count=-1, save=False)

    player_game.save()


def send_message_status(catan_event, room_name=None, turn=None):
    if turn is None:
        turn = catan_event.turn.id

    if room_name is None:
        room_name = catan_event.event.room_name
    send_message(room_name=room_name, message={"turn": turn, "action": catan_event.state, "args": {}})


def pop_random_development_card(catan_event: models.CatanEvent):
    development_cards = ["knight" for k in range(catan_event.all_knight_card)]
    development_cards.extend(["monopoly" for m in range(catan_event.all_monopoly_card)])
    development_cards.extend(["road_building" for r in range(catan_event.all_road_building)])
    development_cards.extend(["year_of_plenty" for y in range(catan_event.all_year_of_plenty)])
    development_cards.extend(["victory" for v in range(catan_event.all_victory_card)])
    random.shuffle(development_cards)
    card = development_cards[0]

    if card == "knight":
        catan_event.all_knight_card -= 1
    elif card == "monopoly":
        catan_event.all_monopoly_card -= 1
    elif card == "road_building":
        catan_event.all_road_building -= 1
    elif card == "year_of_plenty":
        catan_event.all_year_of_plenty -= 1
    elif card == "victory":
        catan_event.all_victory_card -= 1

    catan_event.save()


def check_finish(catan_event: models.CatanEvent):
    for player in catan_event.playergame_set.all():
        if get_point(player_game=player) >= 10:
            catan_event.state = "finish"
            catan_event.save()
            # send_message_status(catan_event=catan_event, room_name=catan_event.event.room_name)
            return player

    return None


def get_longest_road(player_game: models.PlayerGame):
    roads = player_game.road_set.all()
    DG = nx.DiGraph()
    for road in roads:
        DG.add_edge(road.vertex1, road.vertex2, weight=1)
    nodes = nx.dag_longest_path(DG, weight='weight')
    if len(nodes) <= 0:
        return 0

    else:
        return len(nodes) - 1


def shuffle_numbers():
    place6_1, place6_2, place8_1, place8_2 = find_place_for_6_8()

    others = [2, 3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11, 12]
    random.shuffle(others)
    result = []
    j = 0
    for i in range(18):
        if i == place6_1:
            result.append(6)
        elif i == place6_2:
            result.append(6)
        elif i == place8_1:
            result.append(8)
        elif i == place8_2:
            result.append(8)
        else:
            result.append(others[j])
            j += 1

    return result

    # TODO write shuffle
    # return [10, 2, 9, 12, 6, 14, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]
    # return [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]


def not_neighbor_list(number, can_accept_list):
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
    tiles = [[], t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19]
    result = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    # numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    return [x for x in can_accept_list if (x != number and x not in tiles[number])]


def find_place_for_6_8():
    threshold = 4
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    result = []
    for i in range(0, 4):
        if threshold == 0:
            return [4, 10, 11, 16]

        if len(numbers) != 0:
            number = random.choice(numbers)
            numbers = not_neighbor_list(number, numbers)
            result.append(number)
        else:
            threshold -= 1

    return [x - 1 for x in result]


def update_longest_road(catan_event: models.CatanEvent):
    try:
        player_has_longest_road = catan_event.playergame_set.get(has_long_road_card=True)
        longest_road = get_longest_road(player_game=player_has_longest_road)
    except:
        player_has_longest_road = None
        longest_road = 0
    for player in catan_event.playergam_set.all():
        player_road_length = get_longest_road(player)
        if player_road_length > longest_road and player_road_length > 4:
            if player_has_longest_road is not None:
                player_has_longest_road.has_long_road_card = False
                player_has_longest_road.save()
            player_has_longest_road = player
            longest_road = player_road_length
            player.has_long_road_card = True
            player.save()

    return [player_has_longest_road, longest_road]


def update_largest_army(catan_event: models.CatanEvent):
    try:
        player_has_largest_army = catan_event.playergame_set.get(has_largest_army=True)
        largest_army = get_longest_road(player_game=player_has_largest_army)
    except:
        player_has_largest_army = None
        largest_army = 0

    for player in catan_event.playergame_set.all():
        player_army = player.knight_card_played
        if player_army > largest_army and player_army > 2:
            if player_has_largest_army is not None:
                player_has_largest_army.has_largest_army = False
                player_has_largest_army.save()

            player.has_largest_army = True
            player.save()
            player_has_largest_army = player
            largest_army = player_army

    return [player_has_largest_army, largest_army]


