import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError, ExpiredSignatureError, jwt
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set")

ALGORITHM = "HS256"


def create_access_token(user_id: str):
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=15),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not payload:
            raise HTTPException(status_code=404, detail="Not found")

    except ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token expired") from err

    except JWTError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err

    if payload.get("type") != expected_type:
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def generate_refresh_token():
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, token_hash


def hash_refresh_token(raw_token: str):
    return hashlib.sha256(raw_token.encode()).hexdigest()
