#!/usr/bin/env python

from flask import Flask
from telegram.ext import CommandHandler, Updater

from bot import APPNAME, PORT, TOKEN, error, schedule

app = Flask(__name__)


@app.route('/wake/', methods=['GET'])
def wake():
    return 'waking'


if __name__ == '__main__':
    app.run()

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(CommandHandler('turni', schedule))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(f'https://{APPNAME}.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
