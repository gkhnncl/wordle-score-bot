from dotenv import load_dotenv
from os import environ

load_dotenv()
SHEET_URL = environ.get("SHEET_URL")

if SHEET_URL is not None:
    try:
        import gspread
    except ImportError:
        print("Missing dependencies. Install gspread for Google Sheets integration.")


def log_scores_gsheet(score):
    """Log score on Google Sheets."""
    gc = gspread.oauth(credentials_filename="credentials.json")
    sh = gc.open_by_url(SHEET_URL)
    sh.sheet1.append_row([score.date, score.user, score.edition, score.score])
    return None
