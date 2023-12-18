from django.contrib import admin

from .models import Gamer, Sortition, Game, PriceRange
from .services import create_draw


class GamerInline(admin.StackedInline):
    model = Gamer
    extra = 0


class PriceRangeInlines(admin.TabularInline):
    model = PriceRange.games.through
    extra = 0
    raw_id_fields = ('pricerange',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [
        GamerInline, PriceRangeInlines
    ]
    exclude = ('price_ranges',)

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
    raw_id_fields = ('creator', 'game_name')


@admin.register(Sortition)
class SortitionAdmin(admin.ModelAdmin):
    pass
