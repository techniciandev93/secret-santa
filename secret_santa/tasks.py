from .celery import app
from telegram_bot.models import Game, Gamer, Sortition
from .make_sortition import main_separated
from celery.schedules import crontab
import datetime


@app.task
def add():
    all_games = Game.objects.all()
    today = datetime.date.today().isoformat()

    for game in all_games:
        game.registration_period = '2023-12-15' #для тестов
        if today == game.registration_period:
            gamers = game.gamers.all()
            users = [user.id for user in gamers]
            donator_ids = main_separated(users)
            print(donator_ids)
            for donator_id in donator_ids:
                sortition = Sortition(
                    game_name=game,
                    gifter=Gamer.objects.get(id=donator_id),
                    recipient=Gamer.objects.get(id=donator_ids[donator_id])
                )
                sortition.save()

