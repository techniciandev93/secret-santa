from django.utils.timezone import localtime

from telegram_bot.bot_logic.loader import bot
from telegram_bot.models import Sortition, Game


def generator_separated_users(users):
    while True:
        for user in users:
            yield user


def get_user(gen_user, user, separated_users):
    while True:
        next_user = next(gen_user)
        if next_user != user and next_user not in separated_users.values():
            return next_user


def separate_players(users):
    separated_users = dict.fromkeys(users, None)

    if len(separated_users) <= 2:
        raise ValueError("Недостаточно участников для жеребьевки")

    user_generator = generator_separated_users(separated_users)
    for user in separated_users:
        value_user = get_user(user_generator, user, separated_users)
        separated_users[user] = value_user
    return separated_users


def create_draw(game):
    current_time = localtime()
    game_instance = Game.objects.filter(pk=game.id, end_registration_period__lte=current_time).first()

    if game_instance:
        if not game_instance.drawing_lots:
            result_separate = separate_players(game.gamers.all())
            game_instance.drawing_lots = True
            game_instance.save()
            for user in result_separate:
                Sortition.objects.get_or_create(
                    game=game,
                    gifter=user,
                    recipient=result_separate[user]
                )
                bot.send_message(user.telegram_id, f'Жеребьевка в игре “Тайный Санта” проведена! Спешу сообщить тебе '
                                                   f'выпал:\n'
                                                   f'{result_separate[user].gamer}\n'
                                                   f'Email: {result_separate[user].email}\n'
                                                   f'Желаемый список подарков:\n'
                                                   f'{result_separate[user].vishlist}\n'
                                                   f'Письмо Санте:\n'
                                                   f'{result_separate[user].santa_letter}')
