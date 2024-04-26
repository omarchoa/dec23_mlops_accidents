# imports
import subprocess

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import create_engine

from config import paths


# define input data model for endpoint /label_prediction
class InputDataLabelPred(BaseModel):
    request_id: int
    y_true: int


# define connection to `database` microservice
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://user:password@database:3306/shield_project_db"
)
mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI)


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Scoring")


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check scoring microservice API status")
async def status():
    result = "The scoring microservice API is up."
    return JSONResponse(content=result)


# endpoint - label prediction
@api.post(
    path="/label-prediction",
    tags=["PROCESSES"],
    name="label prediction",
)
async def label_prediction(input_data: InputDataLabelPred):
    ## save input data to json file
    input_data_json_object = input_data.model_dump_json()
    input_data_json_file = "input_data.json"
    with open(input_data_json_file, "w") as file:
        file.write(input_data_json_object)

    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_SCORING_LABEL_PREDICTION, input=input_data_json_file
    )

    ## run shell command and save output to result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())


# endpoint - update f1 score
@api.get(
    path="/update-f1-score",
    tags=["PROCESSES"],
    name="update f1 score",
)
async def update_f1_score():
    ## define shell command
    command = "python {script}".format(script=paths.SCRIPTS_SCORING_UPDATE_F1_SCORE)

    ## run shell command and save output to result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    ## save f1 score from subprocess output
    f1_score = float(str(result.stdout).strip())

    ## save f1 score to `database` microservice
    with mariadb_engine.connect() as connection:
        connection.execute(
            text(f'INSERT INTO f1_score_table (f1_score) VALUES ("{f1_score}");')
        )
        connection.execute(text("COMMIT;"))

    ## return f1 score
    return f1_score


# endpoint - get f1 scores
@api.get(
    path="/get-f1-scores",
    tags=["MICROSERVICES - Scoring"],
    name="get f1 scores",
)
async def get_f1_scores():
    ## get f1 scores from `database` microservice
    with mariadb_engine.connect() as connection:
        results = connection.execute(text("SELECT * FROM f1_score_table;"))
        f1_score_list = [f"{time.timestamp()};{score}" for time, score in results]
        f1_score_list.insert(0, "timestamp;f1-score")
        f1_scores = "\n".join(f1_score_list)

    ## return f1 scores
    return f1_scores
