from telegram_bot.services import create_draw
from .celery import app
from telegram_bot.models import Game

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    #for test only
    'check-every-10-sec': {
        'task': 'secret_santa.tasks.get_sortition',
        'schedule': 10.0,
    },
}


@app.task
def get_sortition():
    all_games = Game.objects.all()

    for game in all_games:
        create_draw(game)
