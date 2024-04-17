from fastapi import FastAPI
from pydantic import BaseModel

# from pathlib import Path
# import sys

# local library
# root_path = Path(os.path.realpath(__file__)).parents[3]
# sys.path.append(os.path.join(root_path, "src", "data"))
import containerdata  # will be at the same level in the container

# ---------------------------- API --------------------------------------------

api = FastAPI(
    title="SHIELD",
    description="API for downloading raw data files",
    version="0.1",
)


@api.get('/status', name="check API", tags=['GET'])
async def is_fonctional():
    """
    check if the API is running
    """
    return {"DATA API is running"}


class YearRange(BaseModel):
    start_year: int
    end_year: int


@api.post('/update_data', tags=['UPDATE'])
async def update_data(year_range: YearRange):
    containerdata.Data(year_range.start_year, year_range.end_year, '/mounted_data_container_side')
    return {"Data updated"}
