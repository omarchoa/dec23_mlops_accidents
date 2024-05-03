# 🛡️ SHIELD


## ℹ️ About

**SHIELD** (_Safety Hazard Identification and Emergency Law Deployment_) is an AI-powered Python app that uses machine learning to predict road accident priority levels, helping law enforcement optimize resources and maximize impact.


## 🧑🏻‍💻 Development Team

**SHIELD** is developed by:

- Fabrice **Charraud** ([@FCharraud](https://github.com/FCharraud))
- Omar **Choa** ([@omarchoa](https://github.com/omarchoa))
- Michael **Deroche** ([@miklderoche](https://github.com/miklderoche))
- Alexandre **Winger** ([@alexandrewinger](https://github.com/alexandrewinger))

**SHIELD** constitutes our final project for the [DataScientest MLOps Program](https://datascientest.com/en/ml-ops-course).


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
│    ├── docker/                        <- Files to build Docker images and run Docker
│    │    │                                containers.
│    │    │
│    │    ├── data-download-prep/       <- Files for the microservice in charge of downloading
│    │    │                                and preparing input data (accidents).
│    │    │
│    │    ├── database/                 <- Files for the database microservice (MariaDB).
│    │    │
│    │    ├── frontend/                 <- Files for the frontend component (Streamlit).
│    │    │
│    │    ├── gateway/                  <- Files for the API gateway and model performance
│    │    │                                monitoring.
│    │    │
│    │    ├── initialization/           <- Files for the microservice in charge of
│    │    │                                initializing the app.
│    │    │
│    │    ├── prediction/               <- Files for the microservice in charge of producing
│    │    │                                predictions (severity) from input data (accidents).
│    │    │
│    │    ├── scoring/                  <- Files for the microservice in charge of labeling
│    │    │                                predictions (severity) and updating ML metrics
│    │    │                                (F1 scores).
│    │    │
│    │    ├── testing/                  <- Files for the microservice in charge of unit
│    │    │                                testing.
│    │    │
│    │    ├── training/                 <- Files for the microservice in charge of model
│    │    │                                training and retraining.
│    │    │
│    │    └── users/                    <- Files for the microservice in charge of user data
│    │                                     management.
│    │
│    └── script/                        <- Tools and utilities for app setup and automation.
```

---

## 🎬 Getting Started for Developers

These instructions are divided into three sections:
- [🐳 Configure the Docker environment](#-configure-the-docker-environment)
- [🛠️ Configure the app backend](#%EF%B8%8F-configure-the-app-backend)
- [🖥️ Explore the Streamlit frontend](#%EF%B8%8F-explore-the-streamlit-frontend)

---

### 🐳 **Configure the Docker environment**

#### 1. Get Docker

[Instructions](https://docs.docker.com/get-docker/) are available in the official Docker documentation.

#### 2. Create a Docker ID

[Instructions](https://docs.docker.com/docker-id/) are available in the official Docker documentation.

_Example:_ [`fabricecharraud`](https://hub.docker.com/u/fabricecharraud)

#### 3. Log in to Docker Hub from your execution environment

Open a terminal window and run the following command, replacing `<username>` and `<password>` with the credentials that you used to create your Docker ID in [Step 2](#2-create-a-docker-id):

```text
docker login -u <username> -p <password>
```

#### 4. Create a Docker Hub repository to host your version of the app

[Instructions](https://docs.docker.com/docker-hub/repos/create/) are available in the official Docker documentation.

_Example:_ [`fabricecharraud/shield`](https://hub.docker.com/r/fabricecharraud/shield)

[Back to instruction menu](#-getting-started-for-developers)

---

### 🛠️ **Configure the app backend**

#### 5. Clone the app's GitHub repository

[Instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for a wide variety of methods are available in the official GitHub documentation, the simplest being the execution of the following command in the directory of your choice:

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

Run the following command:

```shell
pip install -r requirements.txt
```

#### 8. Create the app's directory dependencies

Run the following command:

```shell
mkdir ~/mariadb_data
mkdir ~/logs
```

#### 9. Add the Docker Hub repository's name to your execution environment

In the `src/docker` subdirectory, open the `.env` file and replace the double-quoted string with the name of the Docker Hub repository that you created in [Step 4](#4-create-a-docker-hub-repository-to-host-your-version-of-the-app).

_Example:_

```text
DOCKER_HUB_REPO="fabricecharraud/shield"
```

#### 10. Build the Docker container images and launch the app

Go back to the directory into which you cloned the GitHub repository in [Step 5](#5-clone-the-apps-github-repository) and run the following command:

```shell
docker-compose -f ./src/docker/docker-compose-dev.yml up
```

#### 11. Push the Docker container images to Docker Hub

To upload the Docker container images to the Docker Hub repository created in [Step 4](#4-create-a-docker-hub-repository-to-host-your-version-of-the-app), run the following command:

```shell
docker-compose -f ./src/docker/docker-compose-dev.yml push
```

[Back to instruction menu](#-getting-started-for-developers)

---

### 🖥️ **Explore the Streamlit frontend**

#### 12. Log in to the app

Point your web browser to [`http://localhost:8501/`](http://localhost:8501/).

You should see the following page:

![SHIELD frontend login page](/reports/figures/frontend_login.png)

Use either of the following credential sets to log in:

| User type | _Nom d'utilisateur_ (username) | _Mot de passe_ (password) |
| --- | --- | --- |
| Standard | `fdo` | `c0ps` |
| Administrator | `admin` | `4dmin` |

#### 13. Try out the app features

To test the **basic** feature set, log in as a **standard user**.

You should land on the following page:

![SHIELD frontend landing page - standard](/reports/figures/frontend_std.png)

To test the **full** feature set, log in as an **administrator**.

You should land on the following page:

![SHIELD frontend landing page - administrator](/reports/figures/frontend_admin.png)

#### 14. Stop the app

To stop the app, return to the terminal window that you used to launch it in [Step 10](#10-build-the-docker-container-images-and-launch-the-app) and press `Ctrl + C`.

#### 15. Resume the app

To resume the app, run the same command that you used in [Step 10](#10-build-the-docker-container-images-and-launch-the-app):

```shell
docker-compose -f ./src/docker/docker-compose-dev.yml up
```

#### 16. Shut down the app

To shut down the app, run the same command that you used in [Step 10](#10-build-the-docker-container-images-and-launch-the-app), replacing `up` with `down`:

```shell
docker-compose -f ./src/docker/docker-compose-dev.yml down
```

[Back to instruction menu](#-getting-started-for-developers) \
[Back to top](#%EF%B8%8F-shield)