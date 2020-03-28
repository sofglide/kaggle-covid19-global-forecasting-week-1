"""
Plotting functions
"""
import math

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def plot_by_country(
    data: pd.DataFrame,
    column: str,
    title: str = None,
    kind: str = "line",
    logy: bool = False,
    figsize: tuple = (15, 7),
    **kwargs,
):
    """Groups data by country and plots 1 column as superposed plots
    Parameters
    ----------
    data : pd.DataFrame
        dataframe containging data to plot
    column : str
        column to plot
    title : str, optional
        pyplot title, by default None
    kind : str, optional
        pyplot kind argument, by default "line"
    logy : bool, optional
        pyplot logy argument, by default False
    figsize : tuple, optional
        pyplot figsize argument, by default (15, 7)
    """

    def round_y(y_limits):
        if logy:
            return [
                10 ** math.floor(math.log10(max(0.1, y_limits[0]))),
                10 ** math.ceil(math.log10(y_limits[1])),
            ]

        return [0, math.ceil(y_limits[1])]

    title = title if title else column

    _, ax = plt.subplots(figsize=figsize)
    data_copy = data.copy()
    if data_copy.index.dtype == "timedelta64[ns]":
        data_copy.index = (data_copy.index / pd.Timedelta(1, "d")).astype(int)
        data_copy.index.name = "days"

    grouped_data = data_copy.groupby("country")[column]
    grouped_data.plot(
        kind=kind, logy=logy, legend=True, grid=True, title=title, ax=ax, **kwargs
    )

    x_lim = data_copy.index.min(), data_copy.index.max()
    y_lim = data_copy[column].min(), data_copy[column].max()

    if data_copy.index.dtype == "datetime64[ns]":
        ax.xaxis.set_minor_formatter(mdates.DateFormatter(""))
        # set ticks every week
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU))
        # set major ticks format
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    else:
        ax.set_xlim([0, math.ceil(x_lim[1])])
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    ax.grid("on", which="minor", linestyle="--")
    ax.set(ylabel=column)
    ax.set_ylim(round_y(y_lim))

    plt.show()
