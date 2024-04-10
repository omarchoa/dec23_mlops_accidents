# 🛡️ SHIELD


## ℹ️ About

**SHIELD** (_Safety Hazard Identification and Emergency Law Deployment_) is an AI-powered Python app that uses machine learning to predict road accident priority levels, helping law enforcement optimize resources and maximize impact.


## 🧑🏻‍💻 Development Team

**SHIELD** is developed by:

- Fabrice **Charraud** ([@FCharraud](https://github.com/FCharraud))
- Omar **Choa** ([@omarchoa](https://github.com/omarchoa))
- Michael **Deroche** ([@miklderoche](https://github.com/miklderoche))
- Alexandre **Winger** ([@alexandrewinger](https://github.com/alexandrewinger))

**SHIELD** constitutes our final project for the [DataScientest Machine Learning Engineer Program](https://datascientest.com/en/machine-learning-engineer-course).


## 🏛️ App Architecture

**SHIELD** is designed following the [microservice architecture pattern](https://microservices.io/patterns/microservices.html), with an [API gateway](https://microservices.io/patterns/apigateway.html) serving as the single entry point for all clients, routing requests to the appropriate microservices.

**Figure 1** illustrates the global app architecture.

![SHIELD global architecture](/reports/figures/architecture_v2.png)
<p align="center">
    <b>Figure 1.</b> The global app architecture.
</p>

Each microservice runs in its own Docker container. Requests are handled by a dedicated micro-API in the container, and data persistence is implemented using Docker volumes. The entire backend (API gateway and microservices) runs on a single Docker network (`shield`).

**Figure 2** illustrates this sub-architecture, taking the `training` microservice as an example.

![Training microservice sub-architecture](/reports/figures/architecture_v2_training.png)
<p align="center">
    <b>Figure 2.</b> The sub-architecture of the <code>training</code> microservice.
</p>


## 🗂️ Repository Tree

The repository is structured as follows:

```text
├── LICENSE
├── README.md                           <- The top-level README for developers using this
│                                          project.
├── docker-compose.yml                  <- Script to launch the `dummy`, `training`,
│                                          `prediction`, and `scoring` microservices.
├── setup_linux.sh                      <- Script to initialize the `dummy`, `training`,
│                                          `prediction`, and `scoring` microservices on Linux.
├── setup_mac.sh                        <- Script to initialize the `dummy`, `training`,
│                                          `prediction`, and `scoring` microservices on Mac.
├── requirements.txt                    <- The requirements file for reproducing the analysis
│                                          environment, e.g. generated with
│                                          `pip freeze > requirements.txt`.
├── test_requirements.txt               <- The requirements file for unit testing.
│
│
├── data/
│    ├── (in .gitignore) cleaned/       <- Intermediate data that has been transformed.
│    ├── (in .gitignore) preprocessed/  <- The final, canonical data sets for modeling.
│    ├── (in .gitignore) raw/           <- The original, immutable data dump.
│    └── sample/                        <- Sample data for testing and debugging.
│
├── logs/                               <- Logs from training and predicting.
│
├── models/                             <- Trained and serialized models, model predictions,
│                                          or model summaries.
│
├── notebooks/                          <- Jupyter notebooks. Naming convention is a number
│                                          (for ordering), the creator's initials, and a short
│                                          `-` delimited description, e.g.
│                                          `1.0-jqp-initial-data-exploration`.
│
├── references/                         <- Data dictionaries, manuals, and all other
│                                          explanatory materials.
│
├── reports/                            <- Generated analysis as HTML, PDF, LaTeX, etc.
│    └── figures/                       <- Generated graphics and figures to be used in
│                                          reporting.
│
├── src/                                <- Source code for use in this project.
│    ├── api/                           <- Scripts for the app prototype (API V1).
│    │
│    ├── config/                        <- Configuration package with helper modules.
│    │
│    ├── data/                          <- Scripts to download or generate data.
│    │
│    ├── docker/                        <- Scripts to build Docker images and run Docker
│    │    │                                containers.
│    │    ├── bdd/                      <- Scripts for the `users` microservice.
│    │    ├── data/                     <- Scripts for the `data` microservice.
│    │    ├── dummy/                    <- Scripts for the `dummy` microservice (for testing
│    │    │                                and debugging).
│    │    ├── main_api/                 <- Scripts for the `gateway` microservice (API V2).
│    │    ├── prediction/               <- Scripts for the `prediction` microservice.
│    │    ├── scoring/                  <- Scripts for the `scoring` microservice.
│    │    ├── training/                 <- Scripts for the `training` microservice.
│    │    ├── all_in_one.sh             <- Script to initialize the `users`, `data`, and
│    │    │                                `gateway` microservices.
│    │    └── docker-compose.yml        <- Script to launch the `users`, `data`, and
│    │                                     `gateway` microservices.
│    │
│    ├── models/                        <- Scripts to train models and then use trained models
│    │                                     to make
│    │                                     predictions.
│    └── scoring/                       <- Scripts for scoring and monitoring.
```


## 🎬 Getting Started

To use the app from the repository root:

### 1. Set up a Python virtual environment

Using Python's `venv` module, with `sword` as the virtual environment name, open a terminal window and run the following commands:

```shell
python -m venv sword
chmod +x ./sword/bin/activate
source ./sword/bin/activate
```

### 2. Install Docker

[Instructions](https://docs.docker.com/get-docker/) for a wide variety of platforms are available on the official Docker website.

### 3. Set up and launch the app

Run the following command:

_On Linux_

```shell
sh setup_linux.sh
```

_On Mac_

```shell
sh setup_mac.sh
```

> [!IMPORTANT]
> `sudo` privileges are required to complete the execution of these scripts.

### 4. Check the status of the microservices

To ping the `training` microservice, open a new terminal window and run the following command:

```shell
curl -X GET i http://0.0.0.0:8004/status
```

You should receive the following response:

```text
"The microservice API is up."
```

> [!NOTE]
> The `prediction` and `scoring` microservices listen on ports `8005` and `8006`, respectively.

### 5. Try out the microservice features

For the `training` microservice, the full, interactive list of endpoints is accessible via its API's Swagger UI at [`http://0.0.0.0:8004/docs`](http://0.0.0.0:8004/docs).

> [!IMPORTANT]
> Certain endpoints require **user authentication**. These can be accessed by passing the following string to the `Identification` field when executing the endpoints: `fdo:c0ps`.
>
> Other endpoints additionally require **administrator authorization**. These can be accessed by passing the following string to the `Identification` field when executing the endpoints: `admin:4dmin`.

> [!NOTE]
> The endpoints for the `prediction` and `scoring` microservices are available on ports `8005` and `8006`, respectively.

### 6. Stop the app

To stop the app, return to the terminal window used to launch it in [Step 4](#4-run-the-setup-script-and-start-up-the-app) and press `Ctrl + C`.

### 7. Resume the app

To resume the app, run the following command:

```shell
docker-compose up
```

### 8. Shut down the app

To shut down the app and remove all associated containers, run the following command:

```shell
docker-compose down
```


<!--


### 7- Run the tests:

`python ./src/features/api/test_api.py`

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

Commands are not available for Windows for now. You will have to test the endpoints by going to http://127.0.0.1:8000/docs in your navigator (please refer to ### 8- for further informations.)

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


-->

