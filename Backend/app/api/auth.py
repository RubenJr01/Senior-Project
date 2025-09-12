from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_db
from app.db import models
router = APIRouter()

@router.post("/register", status_code=201)
def register(body: RegisterIn, db: Session = Depends(get_db)):
  if db.query(models.User).filter_by(email=body.email).first():
    raise HTTPException(status_code=409, detail="Email already registered")
  user = models.User(email=body.email, hashed_password=hash_password(body.password), name=body.name)
  db.add(user); db.commit(); db.refresh(user)
  return {"id": user.id, "email": user.email}

@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
  user = db.query(models.User).filter_by(email=body.email).first()
  if not user or not verify_password(body.password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Invalid credentials")
  return {"accessToken": create_access_token(user.email)}