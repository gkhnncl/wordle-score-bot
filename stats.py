import datetime
import gspread
import pandas as pd

from constants import BASE_ED_DATE
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
    int or float
    """
    try:
        p = abs(int(x[0]) - 6) + 1
    except ValueError:
        p = 0.5

    return p


def convert_points_to_wordle_score(p):
    """Return Wordle score equivalent of points.

    If the given points is not within 1 through 6 or 0.5, None is returned.

    Parameters
    ----------
    p : int or float
        Points to be converted to Wordle score

    Returns
    -------
    str or None
        Wordle score (e.g., "4/6")
    """
    x = None
    if p in range(1, 7):
        x = f"{str(abs(p - 6) + 1)}/6"
    elif p == 0.5:
        x = "X/6"

    return x


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
    agg = df.groupby("username").agg(points=("points", "sum"))
    return agg


def get_top_n_users(df, n=5):
    """Return the top n users from the scores.

    If there are ties at the nth position, users with the same score as the nth user
    will be included.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe of Wordle scores
    n : int, default 5
        Number of positions to include

    Returns
    -------
    pandas.DataFrame
    """
    top_df = get_total_points(df).sort_values("points", ascending=False)

    # Handle ties
    if len(top_df) > n:
        p_bound = top_df["points"].iloc[n - 1]
        top_df = top_df[top_df["points"] >= p_bound]

    return top_df


def _get_recap_df(df):
    """Get top users and return Wordle scores.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe of Wordle scores of a Wordle edition

    Returns
    -------
    pandas.DataFrame
    """
    df = get_top_n_users(df)
    df["score"] = df["points"].apply(lambda x: convert_points_to_wordle_score(x))
    return df[["score"]]


def get_recap():
    """Get leaderboards of the last two editions.

    Returns
    -------
    tuple of (int, pandas.DataFrame, int, pandas.DataFrame)
        Corresponds to (latest-1) edition, (latest-1) leaderboard, latest edition,
        latest leaderboard
    """
    df = get_scores_df()

    ed2 = df["wordle"].max()
    ed1 = ed2 - 1
    lb1 = _get_recap_df(df[df["wordle"] == ed1].copy())
    lb2 = _get_recap_df(df[df["wordle"] == ed2].copy())

    return ed1, lb1, ed2, lb2


def resolve_weekly_edition():
    """Return starting and ending editions for the past week.

    Returns
    -------
    tuple of (int, int)
        Corresponds to beginning edition, ending edition
    """
    yday = datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
    ed2 = BASE_ED_DATE[0] + (yday - BASE_ED_DATE[1]).days
    ed1 = ed2 - 6

    return ed1, ed2


def get_weekly():
    """Get leaderboard of the past week.

    Returns
    -------
    tuple of (int, int, pandas.DataFrame)
        Corresponds to starting edition, ending edition, leaderboard
    """
    ed1, ed2 = resolve_weekly_edition()

    df = get_scores_df()
    df = df[df["wordle"].between(ed1, ed2)].copy()
    lb = get_total_points(df).sort_values("points", ascending=False)

    return ed1, ed2, lb
