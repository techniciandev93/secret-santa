from telebot import types
from telebot.types import Message

from telegram_bot.bot_logic.loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_game_item = types.KeyboardButton('Создать игру')
    markup.add(create_game_item)
    bot.reply_to(message, 'Организуй тайный обмен подарками, запусти праздничное настроение!',
                 reply_markup=markup)
