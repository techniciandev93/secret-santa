from telegram_bot.services import create_draw
from .celery import app
from telegram_bot.models import Game


@app.task
def get_sortition():
    all_games = Game.objects.all()

    for game in all_games:
        create_draw(game)
