from . import models
from . import serializers
from rest_framework import generics, viewsets

generics.ListAPIView.list()


def finish_game(catan_event):
    queryset = models.PlayerGame.objects.filter(catan_event=catan_event)
    for instance in queryset:
        serializer = serializers.PlayerGameSerializer(instance=instance)
        if serializer.data["point"] >= 10:
            return instance

    return None


def allocate_resources(number, catan_event):
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

    tiles = models.Tile.objects.filter(catan_event=catan_event, number=number)

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



