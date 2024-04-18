from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import create_engine


class NewUser(BaseModel):
    username: str
    password: str
    rights: int  # Default rights (e.g: fdo), for admin rights != 0


class OldUser(BaseModel):
    user: str


def get_users_db():
    mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # echo is for debug mode
    with mariadb_engine.connect() as connection:
        results = connection.execute(text('SELECT * FROM users_table;'))
        users_db = {login: {"pwd": pwd, "admin":admin} for login, pwd, admin in results}
    return users_db


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mariadb_container:3306/shield_project_db'


api = FastAPI()


@api.get(
    path="/status",
    tags=["STATUS"],
    name="check users microservice API status"
)
async def status():
    result = "The users microservice API is up."
    return JSONResponse(content=result)


@api.get(
    path="/all",
    tags=["PROCESSES"],
    name="get all users",
)
async def all():
    return get_users_db()


@api.post(
    path="/register",
    tags=["PROCESSES"],
    name="register user"
)
async def register(new_user: NewUser):
    """Add a user in the database"""

    mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # echo is for debug mode
    with mariadb_engine.connect() as connection:
        connection.execute(text(f'INSERT INTO users_table VALUES ("{new_user.username}", "{new_user.password}", "{new_user.rights}");'))
        connection.execute(text('COMMIT;'))
    result = "User added."
    return JSONResponse(content=result)


@api.delete(
    path="/remove",
    tags=["PROCESSES"],
    name="remove user"
)
async def remove(old_user: OldUser):
    """Remove an existing user from the database
    Administrator rights are required to remove a user.
    Identification field shall be fill as following: identifier:password.
    """

    mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # echo is for debug mode
    with mariadb_engine.connect() as connection:
        connection.execute(text(f'DELETE FROM users_table WHERE login = "{old_user.user}";'))
        connection.execute(text('COMMIT;'))
    result = "User removed."
    return JSONResponse(content=result)