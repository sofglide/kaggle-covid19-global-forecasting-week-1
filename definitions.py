from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()
DATA_DIR = "data"

DATASET_NAME = "imdevskp/corona-virus-report"
DATA_FILE = 'covid_19_clean_complete.csv'

MISSING_TOKEN_MSG = """
Cannot access Kaggle data
Make sure you have a Kaggle account, you can create one from here https://kaggle.com
Then you need to generate an access token
For that click on your profile icon in top-right corner
Select 'Account' from the drop-down menu
Scroll down to 'API' section
Click on 'Create New API Token'
Download generated file 'kaggle.json' to '~/.kaggle/'
Change access privileges by executing command 'chmod 600 ~/.kaggle/kaggle.json'
Then restart from here"""
