from pydantic import BaseModel, field_validator
from datetime import datetime

class EventCreate(BaseModel):
  title: str; startAt: datetime; endAt: datetime
  @field_validator("endAt")
  @classmethod
  
  def end_after_start(cls, v, values):
    if "startAt" in values and v <= values["startAt"]:
      raise ValueError("endAt must be after startAt")
    return v
  
class EventOut(BaseModel):
  id: int; title: str; startAt: datetime; endAt: datetime
  class Config: from_attributes = True
  
class EventPage(BaseModel):
  items: list[EventOut]