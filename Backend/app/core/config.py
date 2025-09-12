import os 
from pydantic import BaseModel

class Settings(BaseModel):
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
  JWT_SECRET: str = os.getenv("JWT_SECRET", "password") # This is random for now, we will change accordingly #
  JWT_ALG: str = "HS256"
  ACCESS_TTL_MIN: int = 60
  
settings = Settings()