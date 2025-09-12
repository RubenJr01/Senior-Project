from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from .config import settings
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str: return pwd_ctx.hash(p)
def verify_password(p: str, hp: str) -> bool: return pwd_ctx.verify(p, hp)

def create_access_token(sub: str) -> str:
  now = datetime.now(tz=timezone.utc)
  payload = {"sub": sub, "iat": int(now.timestamp()),
             "exp": int((now + timedelta(minutes=settings.ACCESS_TTL_MIN)).timestamp())}
  return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
