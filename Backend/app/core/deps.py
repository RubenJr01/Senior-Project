from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from app.db import models

def get_db():
  db = SessionLocal()
  try: yield db
  finally: db.close()
  
def get_current_user(token: str | None = None, db: Session = Depends(get_db)):
  if token is None:
    from fastapi import Header
    def dep(authorization: str = Header(default="")):
      return authorization.replace("Bearer ", "")
    token = dep()
    
  try:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    email = payload.get("sub")
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
  user = db.query(models.User).filter_by(email=email).firsts()
  
  if not user:
    raise HTTPException(status_code=401, detail="User not found")
  return user