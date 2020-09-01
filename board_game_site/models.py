from django.db import models
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
import uuid


# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=50)
    min_player = models.IntegerField()
    max_player = models.IntegerField()
    tutorial_video = models.URLField(null=True, blank=True)
    # tutorial_video = models.FileField(upload_to="tutorial_video/", null=True, blank=True)
    tutorial_doc = models.FileField(upload_to="tutorial_doc/", null=True, blank=True)
    logo = models.ImageField(upload_to="logo/")
    slug = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    long_description=models.TextField(null=True , blank=True)
    is_active = models.BooleanField(default=False)

    def clean(self):
        self.tutorial_doc_clean()

    def tutorial_doc_clean(self):
        if self.tutorial_doc is None or len(str(self.tutorial_doc).strip()) == 0:
            return
        if str(self.tutorial_doc).split(".")[-1] not in ("html", "htm", "pdf"):
            raise ValidationError("invalid format for this file ")

    def __str__(self):
        return self.name


class GameImage(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="game_image/")


class GameEvent(models.Model):
    game = models.ForeignKey("Game", on_delete=models.SET_NULL, null=True, blank=True)
    date = jmodels.jDateTimeField(auto_now_add=True)
    room_name = models.UUIDField(default=uuid.uuid4)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}__{}".format(self.game, self.date)


class UserGame(models.Model):
    user = models.ForeignKey("registry.User", on_delete=models.CASCADE)
    game_event = models.ForeignKey("GameEvent", on_delete=models.CASCADE)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return "{}_{}".format(self.user, self.game_event)


class GameVote(models.Model):
    user_game = models.OneToOneField("UserGame", on_delete=models.SET_NULL, null=True, blank=True)
    CHOICE = (
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    )
    vote = models.IntegerField(choices=CHOICE)


class GameComment(models.Model):
    user_game = models.OneToOneField("userGame", on_delete=models.CASCADE)
    comment = models.TextField()
    status_choices = (
        ("c", "checking"),
        ("a", "accept"),
        ("r", "reject")
    )
    status = models.CharField(max_length=1, choices=status_choices , default="c")
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "comment"

    def __str__(self):
        return "{}__{}".format(self.user_game.user, self.user_game.game_event)
