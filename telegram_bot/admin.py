from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from django import forms
import random

from .models import Gamer, Sortition, Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'limit_cost', 'limits', 'registration_period', 'shipping_date']


@admin.register(Gamer)
class GamerAdmin(admin.ModelAdmin):
    list_display = ['game_name', 'gamer']


class SortitionAdmin(admin.ModelAdmin):
    list_display = ['game_name']
    list_display = ('gifter', 'recipient', 'game_name')
    actions = ['change_pair']

    def change_pair(self, request, queryset):
        selected_pairs = list(queryset)
        for pair in selected_pairs:
            pair.gifter, pair.recipient = pair.recipient, pair.gifter
            pair.save()

    change_pair.short_description = "Изменить пару"


admin.site.register(Sortition, SortitionAdmin)
