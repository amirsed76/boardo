from django.db import models


class CatanEvent(models.Model):
    event = models.OneToOneField("board_game_site.GameEvent", on_delete=models.CASCADE)
    state = models.CharField(max_length=30, null=True, blank=True)
    turn = models.ForeignKey("registry.User", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    all_knight_card = models.IntegerField(default=14)
    all_victory_card = models.IntegerField(default=5)
    all_monopoly_card = models.IntegerField(default=2)
    all_year_of_plenty = models.IntegerField(default=2)
    all_road_building = models.IntegerField(default=2)


class PlayerGame(models.Model):
    catan_event = models.ForeignKey("CatanEvent", on_delete=models.CASCADE)
    player = models.ForeignKey("registry.User", on_delete=models.CASCADE)
    brick_count = models.IntegerField(default=0)
    sheep_count = models.IntegerField(default=0)
    stone_count = models.IntegerField(default=0)
    wheat_count = models.IntegerField(default=0)
    wood_count = models.IntegerField(default=0)
    has_long_road_card = models.BooleanField(default=False)
    has_largest_army = models.BooleanField(default=False)
    monopoly_count = models.IntegerField(default=0)
    year_of_plenty = models.IntegerField(default=0)
    road_building_count = models.IntegerField(default=0)
    victory_point = models.IntegerField(default=0)
    knight = models.IntegerField(default=0)
    knight_card_played = models.IntegerField(default=0)
    thief_tile = models.IntegerField(default=0)

    def next(self, reverse=False):
        if reverse:
            players = PlayerGame.objects.filter(catan_event=self.catan_event).reverse()
        else:
            players = PlayerGame.objects.filter(catan_event=self.catan_event)

        for index, player in enumerate(players):
            if player == self.player:
                if index == 3:
                    return players[0].player.id
                else:
                    return players[index + 1].player.id

    class Meta:
        unique_together = ["catan_event", "player"]


class Tile(models.Model):
    catan_event = models.ForeignKey("CatanEvent", on_delete=models.CASCADE)
    identify = models.IntegerField()
    RESOURSESE = {
        ("brick", "brick"),
        ("sheep", "sheep"),
        ("stone", "stone"),
        ("wheat", "wheat"),
        ("wood", "wood"),
        ("desert", "desert")

    }
    resource = models.CharField(max_length=6, choices=RESOURSESE)
    number = models.IntegerField(null=True)


class Settlement(models.Model):
    player_game = models.ForeignKey("PlayerGame", on_delete=models.CASCADE)
    vertex = models.IntegerField()
    CHOICES = {
        ("home", "home"),
        ("city", "city")
    }
    kind = models.CharField(max_length=4, choices=CHOICES)


class Road(models.Model):
    player_game = models.ForeignKey("PlayerGame", on_delete=models.CASCADE)
    vertex1 = models.IntegerField()
    vertex2 = models.IntegerField()


class Trade(models.Model):
    player_game = models.ForeignKey("PlayerGame", on_delete=models.CASCADE)

    brick_want = models.IntegerField(default=0)
    sheep_want = models.IntegerField(default=0)
    stone_want = models.IntegerField(default=0)
    wheat_want = models.IntegerField(default=0)
    wood_want = models.IntegerField(default=0)

    brick_give = models.IntegerField(default=0)
    sheep_give = models.IntegerField(default=0)
    stone_give = models.IntegerField(default=0)
    wheat_give = models.IntegerField(default=0)
    wood_give = models.IntegerField(default=0)


class TradAnswer(models.Model):
    trade = models.ForeignKey("Trade", on_delete=models.CASCADE)
    player = models.ForeignKey("PlayerGame", on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
