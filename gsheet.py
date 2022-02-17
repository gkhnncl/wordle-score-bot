from dotenv import load_dotenv
from os import environ

load_dotenv()
SHEET_URL = environ.get("SHEET_URL")

if SHEET_URL:
    try:
        import gspread
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "Missing dependencies. Install gspread for Google Sheets integration."
        )


def log_scores_gsheet(score):
    """Log score on Google Sheets."""
    gc = gspread.service_account(filename="service_account.json")
    sh = gc.open_by_url(SHEET_URL)
    sh.sheet1.append_row([score.date, score.user, score.edition, score.score])
    return None
