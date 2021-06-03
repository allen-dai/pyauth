from fastapi import FastAPI, Response, HTTPException
from dotenv import load_dotenv

from model import User, UserLogin
from auth import Auth

import pymongo, os, json, uvicorn

load_dotenv()
URL = os.getenv("DB_URL")
DB = os.getenv("DB_NAME")
COLL = os.getenv("COLL_NAME")
client = pymongo.MongoClient(URL)

PWD_SECRET = os.getenv("PWD_SECRET")

app = FastAPI()
auth = Auth()

@app.get("/")
def index():
    return {"message":"Welcome"}

@app.post("/register/")
def register(user: User):
    """
    pymongo - find() will always return a cursor object. List(cursor) to check if is username availble

    return: str
    """
    cursor = client[DB][COLL].find({"username":user.username})
    if list(cursor)!=[]:
        raise HTTPException(status_code=400, detail="Username unavailble")

    #User is a User object from model.py. <class 'model.User'>
    user = user.dict()

    user["password"] = auth.pwd_hash(user["password"].encode("utf-8"))
    client[DB][COLL].insert_one(user)
    return {"message":"Ok, registered"}


@app.post("/login/")
def login(user: UserLogin, response: Response):
    """
    pymongo - find_one() return None if not exist, else JSON/Dict

    return: jwt
    """
    cursor = client[DB][COLL].find_one({"username": user.username, "password": auth.pwd_hash(user.password)})
    if cursor==None:
        raise HTTPException(status_code=400, detail="Invalid username/password")

    token = auth.jwt_encode(user.username)
    response.set_cookie(
            key="Authorization",
            value=f"Bearer {token}",
            httponly=True,
            path="/",
            secure=True
            )
    return {"message":"Login success, token set"}

        





if __name__ == "__main__":
    uvicorn.run("auth:app", host="0.0.0.0", port=6000, reload=True)
