"""downloads data from Kaggle."""

import tempfile
import zipfile
from pathlib import Path
from urllib import parse

import pandas as pd
import wget

from definitions import (
    COUNTRY_POPULATION_CSV,
    COUNTRY_POPULATION_ZIP_CSV,
    DATA_DIR,
    DATASET_NAME,
    MISSING_TOKEN_MSG,
    ROOT_DIR,
    WORLD_POPULATION_URL,
)

try:
    import kaggle
except OSError:
    print(MISSING_TOKEN_MSG)
    raise


def download_data_from_kaggle(
    force: bool = False, quiet: bool = False, unzip=True
) -> Path:
    """Downloads competition data from Kaggle
    Parameters
    ----------
    force : bool, optional
        overwrite exisiting data, by default False
    quiet : bool, optional
        quiet mode, by default False
    unzip : bool, optional
        unzip files, by default True
    Returns
    -------
    Path
        processed file location
    """
    dataset_file = "covid_19_clean_complete.csv"

    data_path = ROOT_DIR / DATA_DIR
    data_path.mkdir(exist_ok=True)

    kaggle.api.dataset_download_files(
        DATASET_NAME, ROOT_DIR / DATA_DIR, force=force, quiet=quiet, unzip=unzip
    )

    return ROOT_DIR / DATA_DIR / dataset_file


def download_JHU() -> Path:
    """Created dataset file from JHU data
    Returns
    -------
    Path
        processed file location
    """

    JHU_urls = {
        "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
        "csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
        "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
        "csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    }

    JHU_files = {}
    for key, url in JHU_urls.items():
        fname = parse.urlparse(url).path.split("/")[-1]
        file_path = ROOT_DIR / DATA_DIR / fname
        JHU_files[key] = file_path
        tmp_file = wget.download(url, out=str(file_path))
        if Path(tmp_file) != file_path:
            Path(tmp_file).rename(file_path)

    JHU_data = {key: pd.read_csv(fname) for key, fname in JHU_files.items()}

    dates = JHU_data["confirmed"].columns[4:]

    conf_df_long = JHU_data["confirmed"].melt(
        id_vars=["Province/State", "Country/Region", "Lat", "Long"],
        value_vars=dates,
        var_name="Date",
        value_name="Confirmed",
    )

    deaths_df_long = JHU_data["deaths"].melt(
        id_vars=["Province/State", "Country/Region", "Lat", "Long"],
        value_vars=dates,
        var_name="Date",
        value_name="Deaths",
    )

    full_table = pd.concat([conf_df_long, deaths_df_long["Deaths"]], axis=1, sort=False)

    # removing canada's recovered values
    full_table = full_table[
        ~full_table["Province/State"].str.contains("Recovered", na=False)
    ]
    # removing county wise data to avoid double counting
    full_table = full_table[~full_table["Province/State"].str.contains(",", na=False)]
    # renaming countries, regions, provinces
    full_table["Country/Region"] = full_table["Country/Region"].replace(
        "Korea, South", "South Korea"
    )
    # new values
    feb_12_conf = {"Hubei": ["2/12/20", "Confirmed", "Province/State", 34874]}
    for key, val in feb_12_conf.items():
        full_table.loc[
            (full_table["Date"] == val[0]) & (full_table[val[2]] == key), val[1]
        ] = val[3]

    full_table_fname = ROOT_DIR / DATA_DIR / "complete_dataset.csv"
    full_table.to_csv(full_table_fname, index=False)

    return full_table_fname


def download_world_population():
    """Download world population data
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        tmp_file = wget.download(WORLD_POPULATION_URL, out=str(tmp_dir))
        with zipfile.ZipFile(tmp_file, "r") as tmp_zip:
            tmp_csv_path = tmp_zip.extract(COUNTRY_POPULATION_ZIP_CSV, tmp_dir)
            Path(tmp_csv_path).rename(ROOT_DIR / DATA_DIR / COUNTRY_POPULATION_CSV)


def get_population() -> pd.Series:
    """Reads world population
    Returns
    -------
    pd.Series
        world population as a series
    """
    population = (
        pd.read_csv(ROOT_DIR / DATA_DIR / COUNTRY_POPULATION_CSV, skiprows=4)
        .loc[:, ["Country Name", "2018"]]
        .dropna(axis=0)
        .set_index("Country Name")
        .rename(index={"United States": "US"})["2018"]
        .astype(int)
    )
    return population


if __name__ == "__main__":
    download_JHU()
    download_world_population()
