#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pathlib
import re

from dotenv import load_dotenv
from gsheet import SHEET_URL, log_scores_gsheet
from os import environ
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Load token
load_dotenv()
TOKEN = environ.get("TOKEN")


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Wordle score bot started!")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def score_listener(update, context):
    """Parse and log scores from messages."""
    score = get_wordle_score(update.message.text)
    user = update.message.from_user["username"]
    if score is not None:
        log_score_csv(score, user)

        if SHEET_URL is not None:
            log_scores_gsheet(score, user)

    return None


def get_wordle_score(text):
    """Return the header if text is a Wordle score."""
    score = re.match(r"Wordle [0-9]+ [0-6]\/[0-6]", text)
    if score is not None:
        score = score.group()

    return score


def log_score_csv(score, user, fpath="scores.csv"):
    """Log score in a local csv file."""
    fpath = pathlib.Path(fpath)

    # Create score file if not yet existing
    if not fpath.exists():
        with open(fpath, "w") as file:
            file.write("username,wordle,score\n")

    with open(fpath, "a") as file:
        log = f"{user},{score.split()[1]},{score.split()[2]}\n"
        file.write(log)

    # TODO: score validation / repeated posts

    return None


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, score_listener))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
