# Project Name: SHIELD

(Safety Hazard Identification and Emergency Law Deployment)

## Project Organization

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── check_structure.py
    │   │   ├── import_raw_data.py
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │   │
    │   │   └── api        <- Scripts for the API and unit tests and auxiliary files.
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── visualize.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py

---

## Steps to follow on Linux:

Convention : All python scripts must be run from the root specifying the relative file path.

### 1- Create a virtual environment using Virtualenv.

    `python -m venv my_env`

### Activate it

    `chmod +x ./my_env/bin/activate
    ./my_env/bin/activate`

### Install the packages from requirements.txt

    `pip install -r requirements.txt`

### 2- Execute import_raw_data.py to import the 4 datasets.

    `python src/data/import_raw_data.py` ### It will ask you to create a new folder, accept it.

### 3- Execute make_dataset.py initializing `./data/raw` as input file path and `./data/preprocessed` as output file path.

    `python src/data/make_dataset.py`

### 4- Execute train_model.py to instanciate the model in joblib format

    `python src/models/train_model.py`

### 5- Run the api:

    `uvicorn --app-dir ./src/features/api api:api --reload --host=127.0.0.1 --port=8000`

### 6- Check if the api is running:

In a new terminal, type:

    `curl -X GET http://127.0.0.1:8000/status`

It should return: "L'api fonctionne."

### 7- Run the tests:

`python ./src/features/api/test_api.py`

### 8- Manually test the api:

In your navigator, go to http://127.0.0.1:8000/docs

You can test all the endpoints. When needed, you will be asked a username and a password. We implemented two types of users:
_ Adminstrator Users: try it with `admin:4dmin`. This user's type can run every endpoint.
_ Standard Users: try it with `fdo:c0ps`. This user's type can only run the following endpoints: /status (which doesn't requires any identification), /predict_from_call, /predict_from_test, /label

### 9- Test the api with terminal command:

All commands are written in the file ./src/features/api/Readme_api.md

## Steps to follow on Windows:

Convention : All python scripts must be run from the root specifying the relative file path.

### 1- Create a virtual environment using Virtualenv.

    `python -m venv my_env`

### Activate it

    `./my_env/Scripts/activate`

### Install the packages from requirements.txt

    `pip install -r .\requirements.txt` ### You will have an error in "setup.py" but this won't interfere with the rest

### 2- Execute import_raw_data.py to import the 4 datasets.

    `python .\src\data\import_raw_data.py` ### It will ask you to create a new folder, accept it.

### 3- Execute make_dataset.py initializing `./data/raw` as input file path and `./data/preprocessed` as output file path.

    `python .\src\data\make_dataset.py`

### 4- Execute train_model.py to instanciate the model in joblib format

    `python .\src\models\train_model.py`

### 5- Run the api:

    `uvicorn --app-dir ./src/features/api api:api --reload --host=127.0.0.1 --port=8000`

### 6- Check if the api is running:

In a new terminal, type:

    `curl.exe -X GET http://127.0.0.1:8000/status`

It should return: "L'api fonctionne."

### 7- Run the tests:

`python ./src/features/api/test_api.py`

### 8- Manually test the api:

In your navigator, go to http://127.0.0.1:8000/docs

You can test all the endpoints. When needed, you will be asked a username and a password. We implemented two types of users:
_ Adminstrator Users: try it with `admin:4dmin`. This user's type can run every endpoint.
_ Standard Users: try it with `fdo:c0ps`. This user's type can only run the following endpoints: /status (which doesn't requires any identification), /predict_from_call, /predict_from_test, /label

### 9- Test the api with terminal command:

## Commands are not available for Windows for now. You will have to test the endpoints by going to http://127.0.0.1:8000/docs in your navigator (please refer to ### 8- for further informations.)

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
