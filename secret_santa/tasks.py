import datetime
from django.core.mail import send_mail
from .celery import app
from .make_sortition import main_separated
from telegram_bot.models import Game, Gamer, Sortition


@app.task
def add():
    all_games = Game.objects.all()
    today = datetime.date.today().isoformat()

    for game in all_games:
        game.registration_period = '2023-12-16' #для тестов
        if today == game.registration_period:
            gamers = game.gamers.all()
            user_ids = [gamer.id for gamer in gamers]
            donator_ids = main_separated(user_ids)

            for donator_id in donator_ids:
                gifter = gamers.get(id=donator_id)
                recipient = gamers.get(id=donator_ids[donator_id])
                sortition = Sortition(
                    game_name=game,
                    gifter=gifter,
                    recipient=recipient
                )
                sortition.save()

                santa_email = gifter.email #переделать на id в телеграме

                message = f'''Привет, {gifter.gamer}!
                Жеребьевка в игре “Тайный Санта” {game.name} проведена! Спешу сообщить кто тебе выпал:
                Его зовут {recipient.gamer}.
                Вот его электронная почта: {recipient.email}.
                Он написал Санте письмо: {recipient.santa_letter}
                Вот что он хочет получить в подарок: {recipient.vishlist}
                '''

                send_mail('Итоги игры "Тайный Санта"', message, 'info@santa.ru', [santa_email]) #заменить на сообщение в телеграм
