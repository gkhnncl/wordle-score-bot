#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pathlib
import re

from dotenv import load_dotenv
from os import environ
from tabulate import tabulate
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from constants import DAYS, TIME
from gsheet import SHEET_URL, log_scores_gsheet
from stats import get_recap, get_weekly

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = environ.get("TOKEN")
CHAT_ID = environ.get("CHAT_ID")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


class WordleScore:
    """Class storing a Wordle Score.

    Parameters
    ----------
    date : str
        Date string
    from_user : telegram.User
        User object
    edition : int
        Wordle edition
    score : str
        Wordle score (e.g., "4/6")
    """

    def __init__(self, date, from_user, edition, score):
        self.date = date
        self.edition = edition
        self.score = score
        # Use first_name + last_name for users without a username
        self.user = (
            from_user["username"]
            or f"{from_user['first_name'] or ''} {from_user['last_name'] or ''}"
        )


def score_listener(update, context):
    """Parse and log scores from messages."""
    header = get_wordle_header(update.message.text)
    if header is not None:
        score = WordleScore(
            date=update.message.date.strftime("%x %X %Z%z"),
            from_user=update.message.from_user,
            edition=header.split()[1],
            score=header.split()[2],
        )
        log_score_csv(score)

        if SHEET_URL:
            log_scores_gsheet(score)

    return None


def get_wordle_header(text):
    """Return the header if text is a Wordle score."""
    header = re.match(r"Wordle [0-9]+ [0-6X]\/[0-6]", text)
    if header is not None:
        header = header.group()

    return header


def log_score_csv(score, fpath="scores.csv"):
    """Log score in a local csv file."""
    fpath = pathlib.Path(fpath)

    # Create score file if not yet existing
    if not fpath.exists():
        with open(fpath, "w") as file:
            file.write("date,username,wordle,score\n")

    with open(fpath, "a") as file:
        log = f"{score.date},{score.user},{score.edition},{score.score}\n"
        file.write(log)

    # TODO: score validation / repeated posts

    return None


def convert_df_to_str(df, **kwargs):
    """Return dataframe as human-readable plain text.

    Parameters
    ----------
    df : pandas.DataFrame

    **kwargs
        These parameters will be passed to `tabulate`

    Returns
    -------
    str
    """
    return tabulate(df, headers="keys", tablefmt="simple", **kwargs)


def recap(update, context):
    """Send the last two editions' leaderboards."""
    ed1, lb1, ed2, lb2 = get_recap()

    msg = (
        f"**Leaderboard for Wordle {ed1}**\n"
        f"```\n{convert_df_to_str(lb1, colalign=('left','center'))}```\n\n"
        f"**Leaderboard for Wordle {ed2}**\n"
        f"```\n{convert_df_to_str(lb2, colalign=('left','center'))}```"
    )

    update.message.reply_text(msg, parse_mode="MarkdownV2")

    return None


def compose_weekly_message():
    """Return past week's leaderboard message string.

    Returns
    -------
    str
    """
    ed1, ed2, lb = get_weekly()

    msg = (
        f"**Weekly leaderboard \(Wordle {ed1}\-{ed2}\)**\n"  # noqa: W605
        f"```\n{convert_df_to_str(lb, colalign=('left','center', 'center'))}```"
    )
    return msg


def weekly(update, context):
    """Send the past week's leaderboard.

    Included editions start from yesterday and 6 days prior.
    """
    msg = compose_weekly_message()
    update.message.reply_text(msg, parse_mode="MarkdownV2")

    return None


def send_weekly_message(context):
    """Send the past week's leaderboard.

    Included editions start from yesterday and 6 days prior.
    """
    msg = compose_weekly_message()
    Bot(token=TOKEN).sendMessage(chat_id=CHAT_ID, text=msg, parse_mode="MarkdownV2")
    return None


def help(update, context):
    """Send the past week's leaderboard.

    Included editions start from yesterday and 6 days prior.
    """
    msg = (
        "*How to play*"
        "\nAdd this bot to your group chat and send your Wordle scores\. Messages "
        "receved containing Wordle XXX Y/6 will be logged\."
        "\n\n*Commands*"
        "\n`/recap` \- Get the leaderboards of the last two Wordle editions\."
        "\n`/weekly` \- Get the leaderboard of the past week\."
        "\n\n*Scoring*"
        "\nThe following table shows how much points a Wordle score is worth\."
        "```\nscore  points"
        "\n-----  ------"
        "\n 1/6      6   "
        "\n 2/6      5   "
        "\n 3/6      4   "
        "\n 4/6      3   "
        "\n 5/6      2   "
        "\n 6/6      1   "
        "\n X/6     0.5 ```"
    )

    update.message.reply_text(msg, parse_mode="MarkdownV2")

    return None


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("recap", recap))
    dp.add_handler(CommandHandler("weekly", weekly))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, score_listener))
    dp.add_error_handler(error)

    # Scheduled messages
    if CHAT_ID:
        j = updater.job_queue
        j.run_daily(send_weekly_message, days=DAYS, time=TIME)

    updater.start_polling()
    updater.idle()

    return None


if __name__ == "__main__":
    main()
