#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple ChatBot using Watson AI.

"""

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import trial as AI

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update, user_data):
    """Send a message when the command /start is issued."""
    response = AI.process_msg('iniziamo')

    # Update the stored context with the latest received from the dialog.
    user_data['context'] = response['context']

    text = response['output']['text'][0]
    update.message.reply_text(text)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def AI_request(bot, update, user_data):
    """Echo the user message."""

    response = AI.process_msg(update.message.text, user_data.get('context', {}))

    # Update the stored context with the latest received from the dialog.
    user_data['context'] = response['context']

    text = response['output']['text'][0]
    update.message.reply_text(text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def reset(bot, update, user_data):
    user_data['context'] = {}
    update.message.reply_text('Contesto resettato, riparti con i saluti ciccio!')


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ["APP_TG_TOKEN"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_user_data=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("reset", reset, pass_user_data=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, AI_request, pass_user_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()