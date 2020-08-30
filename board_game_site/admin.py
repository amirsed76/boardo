from django.contrib import admin
from . import models
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter


class GameImageStackedInline(admin.StackedInline):
    model = models.GameImage
    extra = 1


class GameModelAdmin(admin.ModelAdmin):
    inlines = [GameImageStackedInline]


class VoteStackedInlineAdmin(admin.StackedInline):
    model = models.GameVote
    extra = 1


class CommentStackedInline(admin.StackedInline):
    model = models.GameComment
    extra = 1


class UserGameModelAdmin(admin.ModelAdmin):
    # model = models.UserGame
    inlines = [VoteStackedInlineAdmin, CommentStackedInline]


class UserGameStackedInline(admin.StackedInline):
    model = models.UserGame
    extra = 1


class PlayedGameModelAdmin(admin.ModelAdmin):
    inlines = [UserGameStackedInline]


class CommentModelAdmin(admin.ModelAdmin):
    model = models.GameComment
    list_filter = ["status"]


admin.site.register(models.Game, GameModelAdmin)
admin.site.register(models.UserGame, UserGameModelAdmin)
# admin.site.register(models.UserGame)
admin.site.register(models.GameEvent, PlayedGameModelAdmin)
admin.site.register(models.GameComment, CommentModelAdmin)
admin.site.register(models.GameVote)
