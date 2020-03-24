"""
Plotting functions
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
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
    title = title if title else column

    _, ax = plt.subplots(figsize=figsize)

    data.groupby("country")[column].plot(
        kind=kind, logy=logy, legend=True, grid=True, title=title, ax=ax, **kwargs
    )
    ax.set(ylabel=column)
    # set ticks every week
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    # set major ticks format
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.show()
