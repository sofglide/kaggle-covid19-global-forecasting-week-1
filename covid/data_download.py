"""downloads data from Kaggle."""

from pathlib import Path
from zipfile import ZipFile

from definitions import COMPETITION_NAME, DATA_DIR, MISSING_TOKEN_MSG, ROOT_DIR

try:
    import kaggle
except OSError:
    print(MISSING_TOKEN_MSG)
    raise


def download_data_from_kaggle(force: bool = False, quiet: bool = False) -> None:
    """Downloads competition data from Kaggle

    Parameters
    ----------
    force : bool, optional
        overwrite exisiting data, by default False
    quiet : bool, optional
        quiet mode, by default False
    """
    data_path = ROOT_DIR / DATA_DIR
    data_path.mkdir(exist_ok=True)

    kaggle.api.competition_download_files(
        COMPETITION_NAME, ROOT_DIR / DATA_DIR, force=force, quiet=quiet
    )

    data_file = next(Path(data_path).glob(f"{COMPETITION_NAME}*"))
    with ZipFile(data_file) as zip_obj:
        zip_obj.extractall(path=data_path)


if __name__ == "__main__":
    download_data_from_kaggle()
