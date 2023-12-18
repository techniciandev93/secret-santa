from functools import partial

from django.core.exceptions import ValidationError
from django.utils.timezone import localtime
from telebot import types
from telebot.types import Message
from telegram_bot.bot_logic.loader import bot
from telegram_bot.bot_logic.player_registration import get_name_player
from telegram_bot.models import Game


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    uuid_param = message.text.split(maxsplit=1)[-1]
    try:
        current_time = localtime()
        game_instance = Game.objects.filter(uuid=uuid_param,
                                            start_registration_period__lte=current_time,
                                            end_registration_period__gte=current_time).first()
    except ValidationError:
        game_instance = None

    if game_instance:
        if message.chat.id in game_instance.gamers.all().values_list('telegram_id', flat=True):
            register_game(message, game_instance)
        elif message.chat.id not in Game.objects.all().values_list('gamers__telegram_id', flat=True):
            register_game(message, game_instance)
        else:
            bot.send_message(message.chat.id, 'Ты уже участвуешь в игре!')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('Создать игру')
        markup.add(item)
        bot.send_message(message.chat.id, 'Организуй тайный обмен подарками, запусти праздничное настроение',
                         reply_markup=markup)


def register_game(message, game_instance):
    if game_instance.price_ranges.exists():
        price_range_records = game_instance.price_ranges.all()
        price_range = '\n'.join([f'{price.min_price} - {price.max_price}' for price in price_range_records])
    else:
        price_range = 'Нет'
    bot.send_message(message.chat.id, f'Замечательно, ты собираешься участвовать в игре\n'
                                      f'Название игры: {game_instance.name}\n'
                                      f'Ограничение стоимости подарка: {price_range}\n'
                                      f'Период регистрации: '
                                      f'{localtime(game_instance.start_registration_period).strftime("%Y-%m-%d %H:%M")} '
                                      f'- {localtime(game_instance.end_registration_period).strftime("%Y-%m-%d %H:%M")}\n'
                                      f'Дата отправки подарков: {game_instance.shipping_date}')
    bot.send_message(message.chat.id, 'Введите ваше имя:')
    get_name_player_with_args = partial(get_name_player, game_instance=game_instance)
    bot.register_next_step_handler(message, get_name_player_with_args)
