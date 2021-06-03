import jwt, hashlib, os

from fastapi import HTTPException, Security
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
PWD_SECRET = os.getenv("PWD_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")

class Auth:
    def pwd_hash(self, password):
        return hashlib.sha256(password).hexdigest()

    def jwt_encode(self, username):
        payload = {
                'exp' : datetime.utcnow() + timedelta(days=0, minutes=5),
                'iat' : datetime.utcnow(),
                'sub' : username
                }

        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    def jwt_decode(self, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithm=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, details="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, details="Invalid Token")
