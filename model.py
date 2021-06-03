from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    password: str
    email: str
    create_date: str



class UserLogin(BaseModel):
    username: str
    password: str
