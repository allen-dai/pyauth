from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str
    f_name: str
    l_name: str



class UserLogin(BaseModel):
    username: str
    password: str
