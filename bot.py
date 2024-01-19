#!/usr/bin/env python

import logging
import os
from datetime import date
from functools import wraps
from itertools import cycle

from telegram import Bot
from telegram.parsemode import ParseMode

ROOMS = [('Bagni', 2), ('Cucina', 1), ('Sala', 1)]
USERS = ['Davide', 'Giulia', 'Giulio', 'Marco']
APPNAME = 'cleanuptheworldbriosco'
TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.getenv('BOT_PORT', '8443'))
CHAT_ID = os.getenv('BOT_CHAT_ID')
PARSE_MODE = ParseMode.MARKDOWN_V2

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_schedule():
    y, w, _ = date.today().isocalendar()
    users = cycle(USERS[i % len(USERS)] for i in range(w, len(USERS) + w))
    return (
        '*Pulizie {} \- {}*\n'.format(
            *(date.fromisocalendar(y, w, d).strftime('%d/%m') for d in (1, 7))
        ) + '\n'.join(r + ': ' + ', '.join(next(users) for _ in range(n)) for r, n in ROOMS)
    )


def verify_update_chat_id(func):
    @wraps(func)
    def with_verification(update, context):
        if update.message.chat_id == CHAT_ID:
            return func(update, context)

    return with_verification


@verify_update_chat_id
def schedule(update, context):
    update.message.reply_text(get_schedule(), parse_mode=PARSE_MODE)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def notify():
    bot = Bot(token=TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=get_schedule(), parse_mode=PARSE_MODE)
