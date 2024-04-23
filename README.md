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

![SHIELD global architecture](/reports/figures/architecture_global.png)
<p align="center">
    <b>Figure 1.</b> The global app architecture.
</p>

Each microservice runs in its own Docker container. Requests are handled by a dedicated micro-API in the container, and data persistence is implemented using Docker volumes. The entire backend (API gateway and microservices) runs on a single Docker network (`shield`).

**Figure 2** illustrates this sub-architecture, taking the `training` microservice as an example.

![Training microservice sub-architecture](/reports/figures/architecture_sub_training.png)
<p align="center">
    <b>Figure 2.</b> The sub-architecture of the <code>training</code> microservice.
</p>


## 🗂️ Repository Tree

The repository is structured as follows:

```text
├── LICENSE
│
├── README.md                           <- The top-level README for developers using this
│                                          project.
│
├── requirements.txt                    <- The requirements file for reproducing the analysis
│                                          environment, e.g. generated with `pip freeze >
│                                          requirements.txt`
│
├── .github/
│    │
│    └── workflows/                     <- GitHub workflow files.
│
├── data/
│    │
│    ├── cleaned/ (in .gitignore)       <- Intermediate data that has been transformed.
│    │
│    ├── preprocessed/ (in .gitignore)  <- The final, canonical data sets for modeling.
│    │
│    ├── raw/ (in .gitignore)           <- The original, immutable data dump.
│    │
│    └── sample/                        <- Sample data for testing and debugging.
│
├── logs/                               <- Logs from training and predicting.
│
├── models/ (contents in .gitignore)    <- Trained and serialized models, model predictions,
│                                          or model summaries.
│
├── notebooks/                          <- Jupyter notebooks. Naming convention is a number
│                                          (for ordering), the creator's initials, and a short
│                                          `-` delimited description, e.g. `1.0-jqp-initial-
│                                          data-exploration`.
│
├── references/                         <- Data dictionaries, manuals, and all other
│                                          explanatory materials.
│
├── reports/                            <- Generated analysis as HTML, PDF, LaTeX, etc.
│    │
│    └── figures/                       <- Generated graphics and figures to be used in
│                                          reporting.
│
├── src/                                <- Source code for use in this project.
│    │
│    ├── config/                        <- Configuration package with helper modules.
│    │
│    ├── docker/                        <- Scripts to build Docker images and run Docker
│    │    │                                containers.
│    │    │
│    │    ├── data-download-prep/       <- Scripts for the `data-download-prep` microservice.
│    │    │
│    │    ├── database/                 <- Scripts for the `database` microservice.
│    │    │
│    │    ├── dummy/                    <- Scripts for the `dummy` microservice (for testing
│    │    │                                and debugging).
│    │    │
│    │    ├── gateway/                  <- Scripts for the API gateway.
│    │    │
│    │    ├── prediction/               <- Scripts for the `prediction` microservice.
│    │    │
│    │    ├── scoring/                  <- Scripts for the `scoring` microservice.
│    │    │
│    │    ├── training/                 <- Scripts for the `training` microservice.
│    │    │
│    │    └── users/                    <- Scripts for the `users` microservice.
│    │
│    ├── models/                        <- Scripts to train models and then use trained models
│    │                                     to make predictions.
│    │
│    ├── scoring/                       <- Scripts for model performance scoring.
│    │
│    └── script/                        <- Tools and utilities for app setup and automation.
│
└── tests/                              <- Tools and utilities for unit testing.
```


## 🎬 Getting Started for Developers

These instructions are divided into three sections:
- [🐳 Set up the Docker environment](#-set-up-the-docker-environment)
- [🗃️ Set up the app](#%EF%B8%8F-set-up-the-app)
- [⚙️ Use the app](#%EF%B8%8F-use-the-app)

---

### 🐳 **Set up the Docker environment**

#### 1. Get Docker

[Instructions](https://docs.docker.com/get-docker/) are available in the official Docker documentation.

#### 2. Create a Docker ID for use with Docker Hub

[Instructions](https://docs.docker.com/docker-id/) are available in the official Docker documentation.

_Example:_ [`fabricecharraud`](https://hub.docker.com/u/fabricecharraud)

#### 3. Create a Docker Hub repository to host your version of the app

[Instructions](https://docs.docker.com/docker-hub/repos/create/) are available in the official Docker documentation.

_Example:_ [`fabricecharraud/shield`](https://hub.docker.com/r/fabricecharraud/shield)

#### 4. Add the Docker Hub repository's name to your execution environment

In a terminal window, create an environmental variable named `DOCKER_REGISTRY` and assign to it the name of the Docker Hub repository that you created in [Step 3](#3-create-a-docker-hub-repository-to-host-your-version-of-the-app).

_Example:_

```shell
export DOCKER_REGISTRY="fabricecharraud/shield"
```

[Back to instruction menu](#-getting-started-for-developers)

---

### 🗃️ **Set up the app**

#### 5. Clone the app's GitHub repository

[Instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for a wide variety of methods are available in the official GitHub documentation, the simplest being the execution of the following command:

```shell
git clone https://github.com/omarchoa/dec23_mlops_accidents.git
```

#### 6. Set up a Python virtual environment

Using Python's `venv` module, with `sword` as the virtual environment name, run the following commands:

```shell
python -m venv sword
chmod +x ./sword/bin/activate
source ./sword/bin/activate
```

#### 7. Install the app's global dependencies

From the root directory of your local clone of the GitHub repository, run the following command:

```shell
pip install -r requirements.txt
```

#### 8. Build the Docker container images and launch the app

From the root directory of your local clone of the GitHub repository, run the following command:

```shell
docker-compose -f ./src/docker/docker-compose-dev.yml up
```

#### 9. Push the Docker container images to Docker Hub

To upload the Docker container images to the Docker Hub repository created in [Step 3](#3-create-a-docker-hub-repository-to-host-your-version-of-the-app):
- Open a new terminal window.
- Go to the root directory of your local clone of the GitHub repository.
- Run the following command:

```shell
python ./src/script/push_images.py
```

[Back to instruction menu](#-getting-started-for-developers)

---

### ⚙️ **Use the app**

#### 10. Check service status

To ping the API gateway, run the following command:

```shell
curl -X GET i http://0.0.0.0:8001/gateway/status/
```

You should receive the following response:

```text
"The API gateway is up."
```

#### 11. Try out the microservice features

The full, interactive list of endpoints is accessible via the API gateway's Swagger UI at [`http://0.0.0.0:8001/docs`](http://0.0.0.0:8001/docs).

> [!IMPORTANT]
> Certain endpoints require **user authentication**. These can be accessed by passing the following string to the `Identification` field when executing the endpoints: `fdo:c0ps`.
>
> Other endpoints additionally require **administrator authorization**. These can be accessed by passing the following string to the `Identification` field when executing the endpoints: `admin:4dmin`.

#### 12. Stop the app

To stop the app, return to the terminal window that you used to launch it in [Step 8](#8-build-the-docker-container-images-and-launch-the-app) and press `Ctrl + C`.

#### 13. Resume the app

To resume the app, run the same command that you used in [Step 8](#8-build-the-docker-container-images-and-launch-the-app).

#### 14. Shut down the app

To shut down the app, run the same command that you used in [Step 8](#8-build-the-docker-container-images-and-launch-the-app), replacing `up` with `down`:

```shell
docker-compose -f ./src/docker/docker-compose-dev.yml down
```

[Back to instruction menu](#-getting-started-for-developers)