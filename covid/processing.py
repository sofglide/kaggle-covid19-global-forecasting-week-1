"""Data processing
"""
import pandas as pd


def get_start_date(
    data: pd.DataFrame, column: str, threshold: int = 100
) -> pd.Series:
    """[summary]
    Parameters
    ----------
    data : pd.DataFrame
        [description]
    column : str
        [description]
    threshold : int, optional
        [description], by default 100
    Returns
    -------
    pd.Series
        start dates as series indexed by country
    """
    start_date = data.groupby('country').apply(lambda x: (x[column] >= threshold).idxmax())
    start_date.rename(f'{column}_trigger_date', inplace=True)
    return start_date


def filter_by_trigger_date(
    data: pd.DataFrame, column: str, threshold: int = 100
) -> pd.DataFrame:
    """filters the data keeping rows where 'column' is larger than 'threshold'
    and offsets the date in the index so that day 0 is the first day it happens
    Parameters
    ----------
    data : pd.DataFrame
        dataframe
    column : str
        data column
    threshold : int, optional
        threshold for column, by default 100
    Returns
    -------
    pd.DataFrame
        filtered dataframe
    """
    start_date = get_start_date(data, column, threshold)

    after_start = data.groupby("country", group_keys=False).apply(
        lambda g: g[g.index >= start_date[g.name]]
    )

    after_start = after_start.groupby("country", group_keys=False).apply(
        lambda g: g.set_index(g.index - start_date[g.name])
    )

    return after_start
