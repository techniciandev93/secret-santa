from django.contrib import admin

from .models import Gamer, Sortition, Game, PriceRange
from .services import create_draw


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'limit_cost', 'start_registration_period',
                    'end_registration_period', 'shipping_date']

    actions = ('drawing_lots',)

    @admin.action(description='Провести жеребьевку')
    def drawing_lots(self, request, queryset):
        for game in queryset:
            create_draw(game)


@admin.register(PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
    pass


@admin.register(Gamer)
class GamerAdmin(admin.ModelAdmin):
    pass


@admin.register(Sortition)
class SortitionAdmin(admin.ModelAdmin):
    pass
