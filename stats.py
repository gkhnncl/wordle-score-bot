import gspread
import pandas as pd

from gsheet import SHEET_URL


def get_scores_df():
    """Return scores dataframe from Google Sheets or local csv file.

    Returns
    -------
    pandas.DataFrame
    """
    if SHEET_URL is not None:
        gc = gspread.service_account(filename="service_account.json")
        sh = gc.open_by_url(SHEET_URL)
        df = pd.DataFrame(sh.sheet1.get_all_records())
    else:
        df = pd.read_csv("scores.csv")

    return df


def calculate_points(x):
    """Return points equivalent of a Wordle score.

    The following table shows how much points a Wordle score is worth.

    | score | points |
    |:-----:|:------:|
    |  1/6  |    6   |
    |  2/6  |    5   |
    |  3/6  |    4   |
    |  4/6  |    3   |
    |  5/6  |    2   |
    |  6/6  |    1   |
    |  X/6  |   0.5  |

    Parameters
    ----------
    x : str
        Wordle score (e.g., "4/6")

    Returns
    -------
    int
    """
    try:
        p = abs(int(x[0]) - 6) + 1
    except ValueError:
        p = 0.5

    return p


def get_total_points(df):
    """Calculate the total points of each user.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe of Wordle scores

    Returns
    -------
    pandas.DataFrame
    """
    df["points"] = df["score"].apply(lambda x: calculate_points(x))
    lb = df.groupby("username").agg(points=("points", "sum"))
    return lb


# def get_recap():
#     """Get last two editions' leaderboards."""
#     df = get_scores_df()
