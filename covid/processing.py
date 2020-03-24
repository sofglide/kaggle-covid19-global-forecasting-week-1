"""Data processing
"""
from typing import List, Optional

import pandas as pd


def get_start_date(data: pd.DataFrame, column: str, threshold: int = 100) -> pd.Series:
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
    start_date = data.groupby("country").apply(
        lambda x: (x[column] >= threshold).idxmax()
    )
    start_date.rename(f"{column}_trigger_date", inplace=True)
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


def filter_data_by_countries(
    data: pd.DataFrame,
    countries: Optional[List[str]] = None,
    countries_with_states: Optional[List[str]] = None,
    states: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Selects data based on a list of countries
    Parameters
    ----------
    data : pd.DataFrame
        dataset
    countries : List[str], optional
        countries with mainland only, by default None
    countries_with_states : List[str], optional
        countries with multiple states (will be aggregated by sum), by default None
    states : List[str], optional
        states to be considered individually, by default None
    Returns
    -------
    pd.DataFrame
        filtered datadframe
    """
    countries = countries if countries else []
    countries_with_states = countries_with_states if countries_with_states else []
    states = states if states else []

    columns = ["country", "date", "cases", "deaths"]

    data_no_states = data.loc[
        data.country.isin(countries)
        & ((data.country == data.state) | data.state.isna()),
        columns,
    ]
    data_no_states = data_no_states.set_index("date")

    data_multi_states = (
        data.loc[data.country.isin(countries_with_states), columns]
        .groupby(["date", "country"])
        .sum()
    )
    data_multi_states = data_multi_states.reset_index(level=1)

    data_single_states = data.loc[data.state.isin(states)].copy()
    data_single_states.drop(columns="country", inplace=True)
    data_single_states.rename(columns={"state": "country"}, inplace=True)
    data_single_states = data_single_states.loc[:, columns]
    data_single_states.set_index("date", inplace=True)

    return pd.concat([data_no_states, data_multi_states, data_single_states])
