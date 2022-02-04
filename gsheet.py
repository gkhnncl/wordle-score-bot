from dotenv import load_dotenv
from os import environ

load_dotenv()
SHEET_URL = environ.get("SHEET_URL")

if SHEET_URL is not None:
    try:
        import gspread
    except ImportError:
        print("Missing dependencies. Install gspread for Google Sheets integration.")


def log_scores_gsheet(score, user):
    """Log score on Google Sheets."""
    gc = gspread.oauth()
    sh = gc.open_by_url(SHEET_URL)
    sh.sheet1.append_row([user, score.split()[1], score.split()[2]])
    return None
