from . import models
from rest_framework import serializers
from django.db.models import Avg
import registry.models as registry_models
# import registry.serializers as registry_serializers
from django.contrib.sites.models import Site


class GameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameImage
        fields = ["image"]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ["id", "name", "logo", "description"]


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user_game.user", read_only=True)
    # user_avatar = serializers.ImageField(source="user_game.user.avatar.avatar", read_only=True)
    user_avatar = serializers.SerializerMethodField(read_only=True , method_name="get_image")

    class Meta:
        model = models.GameComment
        fields = ["user_name", "user_avatar", "comment", "date"]

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.user_game.user.avatar.avatar.url)


class GameDetailSerializer(GameSerializer):
    mean_vote = serializers.SerializerMethodField(source="get_mean_vote")
    images = GameImageSerializer(read_only=True, source="gameimage_set", many=True)
    comments = serializers.SerializerMethodField("get_comments")

    # comments=CommentSerializer(many=True,source="")

    class Meta:
        model = models.Game
        fields = "__all__"

    def get_comments(self, instance):
        qs = models.GameComment.objects.filter(status="a", user_game__game_event__game=instance)
        serializer = CommentSerializer(instance=qs, many=True,context=self.context)
        return serializer.data

    def get_mean_vote(self, obj):
        votes = models.GameVote.objects.filter(user_game__game_event__game=obj)
        mean = votes.aggregate(Avg('vote'))
        return mean["vote__avg"]


class UserGameSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source="game_event.date", read_only=True)
    game_logo = serializers.ImageField(source="game_event.game.logo", read_only=True)
    game_name = serializers.CharField(source="game_event.game.name", read_only=True)

    class Meta:
        model = models.UserGame
        fields = "__all__"


class GameEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameEvent
        fields = "__all__"
