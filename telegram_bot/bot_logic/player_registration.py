import collections

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.timezone import localtime

from telegram_bot.bot_logic.loader import bot
from telegram_bot.models import Gamer

player_data = collections.defaultdict(dict)


def get_name_player(message, game_instance):
    if message.text and message.text.strip():
        player_data[message.chat.id]['name'] = message.text
        player_data[message.chat.id]['telegram_id'] = message.chat.id
        player_data[message.chat.id]['game_instance'] = game_instance
        bot.send_message(message.chat.id, 'Введите ваш email: ')
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите ваше имя (не оставляйте поле пустым).')
        bot.register_next_step_handler(message, get_name_player)


def get_email(message):
    email = message.text.strip()
    if check_email(email):
        player_data[message.chat.id]['email'] = email
        bot.send_message(message.chat.id, 'Напишите список желаемых подарков: ')
        bot.register_next_step_handler(message, get_wishlist)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректный email')
        bot.register_next_step_handler(message, get_email)


def check_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def get_wishlist(message):
    if message.text and message.text.strip():
        player_data[message.chat.id]['vishlist'] = message.text
        bot.send_message(message.chat.id, 'Напишите мини-письмо Санте: ')
        bot.register_next_step_handler(message, get_santa_letter)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, напишите список желаемых подарков (не оставляйте поле пустым).')
        bot.register_next_step_handler(message, get_wishlist)


def get_santa_letter(message):
    if message.text and message.text.strip():
        player_data[message.chat.id]['santa_letter'] = message.text
        create_gamer(player_data[message.chat.id])
        date = localtime(player_data[message.chat.id]['game_instance'].end_registration_period).strftime("%Y-%m-%d %H:%M")
        bot.send_message(message.chat.id, f"Превосходно, ты в игре! "
                                          f"{date} мы "
                                          f"проведем жеребьевку и ты узнаешь имя"
                                          f"и контакты своего тайного друга. Ему и нужно будет подарить подарок!")
        del player_data[message.chat.id]
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, напишите мини-письмо Санте (не оставляйте поле пустым).')
        bot.register_next_step_handler(message, get_santa_letter)


def create_gamer(player):
    if Gamer.objects.filter(telegram_id=player['telegram_id'], game_name__isnull=True).exists():
        Gamer.objects.update_or_create(
            telegram_id=player['telegram_id'],
            defaults={'gamer': player['name'],
                      'email': player['email'],
                      'vishlist': player['vishlist'],
                      'santa_letter': player['santa_letter'],
                      'game_name': player['game_instance']
                      }
        )
    else:
        Gamer.objects.update_or_create(
            telegram_id=player['telegram_id'],
            game_name=player['game_instance'],
            defaults={'gamer': player['name'],
                      'email': player['email'],
                      'vishlist': player['vishlist'],
                      'santa_letter': player['santa_letter'],
                      }
        )
