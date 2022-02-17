import datetime

# BASE_ED_DATE : tuple of (edition, datetime) - used for computing stats
BASE_ED_DATE = (238, datetime.date(2022, 2, 12))

# Scheduled message settings
# DAYS : tuple of int - Defines which days of the week to send weekly leaderboard
# message. 0-6 correspond to Monday-Sunday
DAYS = (4,)
# TIME : datetime.time - Defines time of day to send weekly leaderboard message.
TIME = datetime.time(4, 0)
