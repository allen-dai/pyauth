from fastapi import FastAPI, Response, HTTPException
from dotenv import load_dotenv

from model import User, UserLogin
from auth import Auth

import pymongo, os, json

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
    cusor = client[DB][COLL].find({"username":user.username})
    if cursor!=None:
        raise HTTPException(status_code=400, detail="Username unavailble")
    user = user.dict()
    user["password"] = auth.pwd_hash(user.password.encode("utf-8"))
    client[DB][COLL].insert_one(user.dict())
    return {"message":"Ok, registered"}

@app.post("/login/")
def login(user: UserLogin, response: Response):
    cursor = client[DB][COLL].find_one({"username": auth.pwd_hash(user.username.encode("utf-8")), "password": user.password})
    if cursor!=None:
        token = auth.jwt_encode(user.username)
        response.set_cookie(key="token", value=token)
        return {"message":"Login success, token set"}

    return {"message":"Invalid Username/Password"}
        





if __name__ == "__main__":
    uvicorn.run("auth:app", host="0.0.0.0", port=6000, reload=True)
