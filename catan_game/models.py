from django.db import models


class CatanEvent(models.Model):
    event = models.OneToOneField("board_game_site.GameEvent", on_delete=models.CASCADE)
    state = models.CharField(max_length=30)
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

