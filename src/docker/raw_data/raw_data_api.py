from fastapi import FastAPI
import json
import os
# from pathlib import Path
# import sys

# local library
# root_path = Path(os.path.realpath(__file__)).parents[3]
# sys.path.append(os.path.join(root_path, "src", "data"))
import containerdata  # will be at the same level in the container
# ---------------------------- HTTP Exceptions --------------------------------
# responses = {
#     200: {"description": "OK"},
#     401: {"description": "Invalid login or password"}
# }

# ---------------------------- Upload users database --------------------------
# with open('/mounted_data_container_side/users_db_bis.json', 'r') as file:
#     users_db = json.load(file)

# ---------------------------- API --------------------------------------------

api = FastAPI(
    title="SHIELD",
    description="API for downloading raw data files",
    version="0.1",
)


@api.get('/status', name="check API", tags=['GET'])
async def is_fonctional():
    """
    to check if the API is running
    """
    return {"API is running"}


@api.get('/download')  # TODO should be a post with years
async def download_raw_data():
    containerdata.Data(2021, 2021, '/mounted_data_container_side') # TODO
    return {"Done"}
