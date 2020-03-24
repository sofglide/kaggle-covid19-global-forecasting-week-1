"""downloads data from Kaggle."""

from definitions import DATA_DIR, DATASET_NAME, MISSING_TOKEN_MSG, ROOT_DIR

try:
    import kaggle
except OSError:
    print(MISSING_TOKEN_MSG)
    raise


def download_data_from_kaggle(
    force: bool = False, quiet: bool = False, unzip=True
) -> None:
    """Downloads competition data from Kaggle

    Parameters
    ----------
    force : bool, optional
        overwrite exisiting data, by default False
    quiet : bool, optional
        quiet mode, by default False
    unzip : bool, optional
        unzip files, by default True
    """
    data_path = ROOT_DIR / DATA_DIR
    data_path.mkdir(exist_ok=True)

    kaggle.api.dataset_download_files(
        DATASET_NAME, ROOT_DIR / DATA_DIR, force=force, quiet=quiet, unzip=unzip
    )


if __name__ == "__main__":
    download_data_from_kaggle()
