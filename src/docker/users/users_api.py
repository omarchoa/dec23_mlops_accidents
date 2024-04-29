# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import create_engine


# define input data model for endpoint /register
class NewUser(BaseModel):
    username: str
    password: str
    rights: int


# define input data model for endpoint /remove
class OldUser(BaseModel):
    user: str


# define database connection
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://user:password@database:3306/shield_project_db"
)
mariadb_engine = create_engine(
    SQLALCHEMY_DATABASE_URI, echo=False
)  # echo is for debug mode


# define function to get all users from database
def get_users_db():
    with mariadb_engine.connect() as connection:
        results = connection.execute(text("SELECT * FROM users_table;"))
        users_db = {
            login: {"pwd": pwd, "admin": admin} for login, pwd, admin in results
        }
    return users_db


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Users")


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check users microservice API status")
async def status():
    result = "The users microservice API is up."
    return JSONResponse(content=result)


# endpoint - all
@api.get(
    path="/all",
    tags=["PROCESSES"],
    name="get all users",
)
async def all():
    return get_users_db()


# endpoint - register
@api.post(path="/register", tags=["PROCESSES"], name="register user")
async def register(new_user: NewUser):
    """Add a user to the database."""

    with mariadb_engine.connect() as connection:
        connection.execute(
            text(
                f'INSERT INTO users_table VALUES ("{new_user.username}", "{new_user.password}", "{new_user.rights}");'
            )
        )
        connection.execute(text("COMMIT;"))
    result = "User added."
    return JSONResponse(content=result)


# endpoint - remove
@api.delete(path="/remove", tags=["PROCESSES"], name="remove user")
async def remove(old_user: OldUser):
    """Remove a user from the database."""

    with mariadb_engine.connect() as connection:
        connection.execute(
            text(f'DELETE FROM users_table WHERE login = "{old_user.user}";')
        )
        connection.execute(text("COMMIT;"))
    result = "User removed."
    return JSONResponse(content=result)
