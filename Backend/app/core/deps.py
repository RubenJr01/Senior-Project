from fastapi import Depends, HTTPException, status, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .config import settings
from ..db.session import SessionLocal
from ..db import models

def get_db():
  db = SessionLocal()
  try: yield db
  finally: db.close()
  
def get_current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)):
  token = authorization.replace("Bearer ", "").strip()
  if not token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

  try:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    email = payload.get("sub")
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

  if not email:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

  user = db.query(models.User).filter_by(email=email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
  return user
