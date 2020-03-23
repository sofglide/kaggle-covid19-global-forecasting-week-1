# kaggle-covid19-global-forecasting-week-1

Kaggle competition covid19-global-forecasting-week-1

## How to use

- Clone the repo
- Create environment executing command ```make env-create```
- Install dependencies calling ```make env-update```
- Activate virtualvenv calling ```source .venv/bin/activate```
- To deactivate it, execute ```deactivate```

Files are distributed as follows:

- Code is under `covid/`
- Notebooks are under `notebooks/`
- Data is not included in the repo, it can be downloaded using ```covid.data_download.download_data_from_kaggle``` and it will be located under ```data```

## How to contribute

- Make a branch with your intended changes
- Create a pull request, get it approved, then merge to the master branch

## Build checks

- Execute command ```make lint```
- If the above complains about formatting, excute ```make reformat``` then execute the previous command again
