from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import create_engine


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mariadb_container:3306/shield_project_db'
# ---------------------------- HTTP Exceptions --------------------------------
responses = {
    200: {"description": "Valid return"},
    401: {"description": "Invalid password"}
}

api = FastAPI()

def get_users_db():
    mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # echo is for debug mode
    with mariadb_engine.connect() as connection:
        results = connection.execute(text('SELECT * FROM users_table;'))
        users_db = {login: {"pwd": pwd, "admin":admin} for login, pwd, admin in results}
    return users_db


@api.get('/status', name="Check whether the main API is running", tags=['GET'])
async def is_fonctionnal():
    return "The users API is up."


@api.get('/users_db', name="Get all database users", tags=['GET'])
async def check():
    return get_users_db()


class User(BaseModel):
    username: str
    password: str
    rights: int  # Default rights (e.g: fdo), for admin rights != 0


@api.post('/register', name="Add a user in the database", tags=['USERS'], responses=responses)
async def post_user(new_user: User):
# async def post_user(username=username, password=password, rights=rights):
#async def post_user(new_user: User, identification=Header(None)):
    """Add a user in the database"""
    # verify_admin_rights(identification)

    mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # echo is for debug mode
    with mariadb_engine.connect() as connection:
        connection.execute(text(f'INSERT INTO users_table VALUES ("{new_user.username}", "{new_user.password}", "{new_user.rights}");'))
        # connection.execute(text(f'INSERT INTO users_table VALUES ("{username}", "{password}", "{rights}");'))
        connection.execute(text('COMMIT;'))
    return "User added"


class OldUser(BaseModel):
    user: str


@api.delete('/remove', name="Remove an existing user from the database", tags=['USERS'], responses=responses)
async def remove_user(old_user: OldUser):
    """Remove an existing user from the database
    Administrator rights are required to remove a user.
    Identification field shall be fill as following: identifier:password.
    """
    # verify_admin_rights(identification)
    mariadb_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # echo is for debug mode
    with mariadb_engine.connect() as connection:
        connection.execute(text(f'DELETE FROM users_table WHERE login = "{old_user.user}";'))
        connection.execute(text('COMMIT;'))
    return "User removed"
