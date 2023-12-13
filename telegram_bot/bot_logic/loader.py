from django.conf import settings
from telebot import StateMemoryStorage, TeleBot

bot_token = settings.TELEGRAM_BOT_API_TOKEN

default_commands = (
    ('start', 'Запустить бота'),
)

state_storage = StateMemoryStorage()
bot = TeleBot(bot_token, state_storage=state_storage)
