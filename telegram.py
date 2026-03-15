from __future__ import annotations

import os

import telebot
from dotenv import load_dotenv


class TelegramNotifier:
    def __init__(self):
        load_dotenv()

        token = os.getenv("Telegram_API")
        users_raw = os.getenv("USERS", "")

        if not token:
            raise ValueError("Telegram_API fehlt in der .env")
        if not users_raw.strip():
            raise ValueError("USERS fehlt in der .env")

        self.bot = telebot.TeleBot(token)
        self.chat_ids = self._parse_chat_ids(users_raw)

    @staticmethod
    def _parse_chat_ids(users_raw: str) -> list[str]:
        normalized = users_raw.replace(";", ",").replace(" ", ",")
        chat_ids = [item.strip() for item in normalized.split(",") if item.strip()]
        if not chat_ids:
            raise ValueError("USERS enthaelt keine gueltigen Chat IDs")
        return chat_ids

    def send_message(self, text: str) -> None:
        for chat_id in self.chat_ids:
            self.bot.send_message(chat_id, text, disable_web_page_preview=False)
