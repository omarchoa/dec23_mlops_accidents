# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import paths
import subprocess


# define input data model for endpoint /call
class InputDataPredCall(BaseModel):
    place: int
    catu: int
    sexe: int
    secu1: float
    year_acc: int
    victim_age: int
    catv: int
    obsm: int
    motor: int
    catr: int
    circ: int
    surf: int
    situ: int
    vma: int
    jour: int
    mois: int
    lum: int
    dep: int
    com: int
    agg_: int
    inter: int
    atm: int
    col: int
    lat: float
    long: float
    hour: int
    nb_victim: int
    nb_vehicules: int


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Prediction")


# endpoint - status
@api.get(
    path="/status", tags=["STATUS"], name="check prediction microservice API status"
)
async def status():
    result = "The prediction microservice API is up."
    return JSONResponse(content=result)


# endpoint - test
@api.get(
    path="/test",
    tags=["PROCESSES"],
    name="predict from test",
)
async def test():
    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_MODELS_PREDICT, input=paths.SAMPLE_FEATURES
    )

    ## define environmental variables
    ### PYTHONPATH and CONTAINERIZED need to be redefined and passed explicitly to the subprocess as its env parameter resets the environmental variables inherited from the container
    env_dict = {
        "PYTHONPATH": "home/shield/src",
        "CONTAINERIZED": "yes",
        "ENDPOINT": "/test",
    }

    ## run shell command and save output to result
    result = subprocess.run(
        command, shell=True, env=env_dict, capture_output=True, text=True
    )

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())


# endpoint - call
@api.post(
    path="/call",
    tags=["PROCESSES"],
    name="predict from call",
)
async def call(input_data: InputDataPredCall):
    # save input data to json file
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
        "ENDPOINT": "/call",
    }

    ## run shell command and save output to result
    result = subprocess.run(
        command, shell=True, env=env_dict, capture_output=True, text=True
    )

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())
