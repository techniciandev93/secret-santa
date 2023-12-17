import collections
import datetime
import re

import telebot_calendar
from django.utils import timezone
from telebot.types import Message, CallbackQuery

from telegram_bot.bot_logic.loader import bot
from telegram_bot.models import Gamer, Game, PriceRange

user_data = collections.defaultdict(dict)

calendar = telebot_calendar.Calendar(language=telebot_calendar.RUSSIAN_LANGUAGE)
calendar_1 = telebot_calendar.CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.datetime.now()


@bot.message_handler(func=lambda message: message.text == 'Создать игру')
def bot_create_game(message: Message) -> None:
    user = Gamer.objects.filter(telegram_id=message.from_user.id, creator__isnull=False).first()
    if user:
        bot.send_message(message.chat.id, 'Введите название игры:')
        bot.register_next_step_handler(message, get_name_game)
    else:
        bot.send_message(message.chat.id, 'Вы не можете создавать игры')


def get_name_game(message):
    if message.text and message.text.strip():
        user_data[message.chat.id]['name'] = message.text
        bot.send_message(message.chat.id, 'Ограничение стоимости подарка: да/нет?')
        bot.register_next_step_handler(message, specify_cost_limit)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите название игры корректно (не оставляйте поле пустым).')
        bot.register_next_step_handler(message, get_name_game)


def specify_cost_limit(message):
    limit = message.text.lower()

    if limit == 'да':
        user_data[message.chat.id]['limit'] = True
        bot.send_message(message.chat.id, 'Введите ограничение стоимости подарка:\n'
                                          'Укажите диапазон через пробел используя дефис (0-500 500-1000 1000-2000)')
        bot.register_next_step_handler(message, get_limit_price)

    elif limit == 'нет':
        user_data[message.chat.id]['limit'] = False
        user_data[message.chat.id]['limit_range'] = None
        get_request_time(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите "да" или "нет".')


def get_limit_price(message):
    price_ranges = parse_price_ranges(message.text)
    if price_ranges:
        user_data[message.chat.id]['limit_range'] = price_ranges
        get_request_time(message)
    else:
        bot.send_message(message.chat.id, 'Введите корректные диапазоны:')
        bot.register_next_step_handler(message, get_limit_price)


def parse_price_ranges(text):
    pattern = r'^(\d+-\d+ ?)+$'
    match = re.match(pattern, text)

    if match:
        ranges = text.split()
        valid_ranges = []

        for range_str in ranges:
            values = range_str.split('-')
            start = int(values[0])
            end = int(values[1])
            valid_ranges.append((start, end))

        return valid_ranges
    else:
        return None


def get_request_time(message):
    bot.send_message(message.chat.id, 'Укажите конечное время регистрации участников\nВведите время в формате ЧЧ:ММ ('
                                      'например, 15:30):')
    bot.register_next_step_handler(message, handle_time_input)


def handle_time_input(message):
    if message.text.count(':') == 1:
        try:
            hour, minute = map(int, message.text.split(':'))
            if 0 <= hour < 24 and 0 <= minute < 60:
                user_data[message.chat.id]['time'] = {'hour': hour, 'minute': minute}
                get_registration_period(message)
            else:
                bot.send_message(message.chat.id, 'Пожалуйста, введите корректное время.')
                bot.register_next_step_handler(message, handle_time_input)
        except ValueError:
            bot.send_message(message.chat.id, 'Пожалуйста, введите время в правильном формате.')
            bot.register_next_step_handler(message, handle_time_input)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите время в формате ЧЧ:ММ.')
        bot.register_next_step_handler(message, handle_time_input)


def get_registration_period(message):
    message = bot.send_message(chat_id=message.chat.id, text='Укажите период регистрации участников:')
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                  reply_markup=calendar.create_calendar(name=calendar_1.prefix,
                                                                        year=now.year,
                                                                        month=now.month))


def get_gift_date(message):
    message = bot.send_message(chat_id=message.chat.id, text='Укажите дату отправки подарка')
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                  reply_markup=calendar.create_calendar(name=calendar_1.prefix,
                                                                        year=now.year,
                                                                        month=now.month))


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == 'DAY':
        if not user_data[call.message.chat.id].get('registration_period'):
            date = date.replace(hour=user_data[call.message.chat.id]['time']['hour'],
                                minute=user_data[call.message.chat.id]['time']['minute'])
            user_data[call.message.chat.id]['registration_period'] = date
            get_gift_date(call.message)
        else:
            user_data[call.message.chat.id]['gift_date'] = date
            instance_game = create_game(user_data[call.message.chat.id])
            bot.send_message(call.message.chat.id, f'Отлично, Тайный Санта уже готовится к раздаче подарков!\nСсылка '
                                                   f'для регистрации'
                                                   f' https://t.me/{bot.get_me().username}?start={instance_game.uuid}')
            del user_data[call.message.chat.id]
    elif action == 'CANCEL':
        if not user_data[call.message.chat.id].get('registration_period'):
            get_registration_period(call.message)
        if not user_data[call.message.chat.id].get('gift_date'):
            get_gift_date(call.message)


def create_game(game_data):
    game_params = {
        'name': game_data['name'],
        'limit_cost': game_data['limit'],
        'start_registration_period': timezone.localtime(),
        'end_registration_period': game_data['registration_period'],
        'shipping_date': game_data['gift_date']
    }
    range_prices = []
    if game_data['limit_range']:
        for range_price in game_data['limit_range']:
            price_range_instance, created = PriceRange.objects.get_or_create(min_price=min(range_price),
                                                                             max_price=max(range_price))
            range_prices.append(price_range_instance)

    new_game = Game.objects.create(**game_params)
    new_game.price_ranges.add(*range_prices)
    return new_game
