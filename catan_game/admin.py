from django.contrib import admin
from . import models


# Register your models here.
class PlayerGameStackedInline(admin.StackedInline):
    model = models.PlayerGame
    extra = 1


class CatanEventAdmin(admin.ModelAdmin):
    inlines = [PlayerGameStackedInline]


admin.site.register(models.CatanEvent, CatanEventAdmin)
