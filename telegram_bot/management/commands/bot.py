from django.core.management import BaseCommand
from telebot.types import BotCommand

from telegram_bot.bot_logic.loader import bot, default_commands


class Command(BaseCommand):
    help = 'Команда для запуска Telegram-бота.'

    def handle(self, *args, **kwargs):
        bot.set_my_commands([BotCommand(*command) for command in default_commands])
        bot.infinity_polling(skip_pending=True)
