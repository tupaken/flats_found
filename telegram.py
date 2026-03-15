import telebot
import os 
from dotenv import load_dotenv

class BotManager():

    def __init__(self):
        self.bot=telebot.TeleBot(os.getenv("Telegram_API"))
        self.users=os.getenv("Users")
    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            if message.chat.id in self.users:
                self.bot.send_message(message.chat.id,"Hi, I send you new flats")
                



