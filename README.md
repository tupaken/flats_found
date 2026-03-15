## Leipzig Flat Monitor

Der Monitor prueft alle 10 Minuten neue Leipziger Sozialwohnungen und sendet Neufunde an Telegram.

### Setup

1. `.env` anlegen:

```env
Telegram_API=<dein_bot_token>
USERS=<chat_id_1,chat_id_2>
```

2. Monitor starten:

```bash
python3 monitor.py
```

Beim ersten Start werden nur die aktuell vorhandenen Wohnungen als Basis gespeichert (`seen_flats.json`), ohne Telegram-Nachricht. Danach werden nur neue Eintraege gesendet.
