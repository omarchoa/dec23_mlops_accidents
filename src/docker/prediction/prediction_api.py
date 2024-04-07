# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import paths
import subprocess


# create fastapi instance
api = FastAPI(
    title="SHIELD Microservice API - Prediction",
    openapi_tags=[
        {"name": "STATUS"},
        {"name": "PROCESSES"},
    ],
)


# define input data model
class InputData(BaseModel):
    place: int = 10
    catu: int = 3
    sexe: int = 1
    secu1: float = 0.0
    year_acc: int = 2021
    victim_age: int = 60
    catv: int = 2
    obsm: int = 1
    motor: int = 1
    catr: int = 3
    circ: int = 2
    surf: int = 1
    situ: int = 1
    vma: int = 50
    jour: int = 7
    mois: int = 12
    lum: int = 5
    dep: int = 77
    com: int = 77317
    agg_: int = 2
    inter: int = 1
    atm: int = 0
    col: int = 6
    lat: float = 48.60
    long: float = 2.89
    hour: int = 17
    nb_victim: int = 2
    nb_vehicules: int = 1


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check microservice status")
async def status():
    result = "The microservice API is up."
    return result


# endpoint - predict from test
@api.get(
    path="/predict_from_test",
    tags=["PROCESSES"],
    name="execute microservice process 1",
)
async def predict_from_test():
    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_MODELS_PREDICT, input=paths.SAMPLE_FEATURES
    )

    ## define environmental variables
    ### PYTHONPATH and CONTAINERIZED need to be redefined and passed explicitly to the subprocess as its env parameter resets the environmental variables inherited from the container
    env_dict = {
        "PYTHONPATH": "home/shield/src",
        "CONTAINERIZED": "yes",
        "ENDPOINT": "/predict_from_test",
    }

    ## run shell command and save output to result
    result = subprocess.run(
        command, shell=True, env=env_dict, capture_output=True, text=True
    )

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())


# endpoint - predict from call
@api.post(
    path="/predict_from_call",
    tags=["PROCESSES"],
    name="execute microservice process 2",
)
async def predict_from_call(input_data: InputData):
    ## save input data to json file
    input_data_json_object = input_data.model_dump_json()
    input_data_json_file = "input_data.json"
    with open(input_data_json_file, "w") as file:
        file.write(input_data_json_object)

    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_MODELS_PREDICT, input=input_data_json_file
    )

    ## define environmental variables
    ### PYTHONPATH and CONTAINERIZED need to be redefined and passed explicitly to the subprocess as its env parameter resets the environmental variables inherited from the container
    env_dict = {
        "PYTHONPATH": "home/shield/src",
        "CONTAINERIZED": "yes",
        "ENDPOINT": "/predict_from_call",
    }

    ## run shell command and save output to result
    result = subprocess.run(
        command, shell=True, env=env_dict, capture_output=True, text=True
    )

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())
