from abc import ABC

from . import models
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer, get_adapter, setup_user_email
import board_game_site.serializers  as board_game_site_serializers


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Avatar
        fields = "__all__"


class CustomRegisterSerializer(RegisterSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.IntegerField(read_only=True, source="user.id")
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    avatar = serializers.IntegerField()

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        clean_data = {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'avatar': self.validated_data.get("avatar")
        }
        return clean_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        try:
            user.avatar = models.Avatar.objects.get(pk=self.cleaned_data["avatar"])
        except:
            pass
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    avatar_detail = AvatarSerializer(read_only=True, source="avatar")
    games = board_game_site_serializers.UserGameSerializer(many=True, source="usergame_set",read_only=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', "avatar", "avatar_detail","games")
        # fields = ('username', 'email', 'first_name', 'last_name')


class USerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
