from pydantic import BaseModel, model_validator
from datetime import datetime

class EventCreate(BaseModel):
  title: str
  startAt: datetime
  endAt: datetime

  @model_validator(mode="after")
  def check_dates(self):
    if self.endAt <= self.startAt:
      raise ValueError("endAt must be after startAt")
    return self
  
class EventOut(BaseModel):
  id: int; title: str; startAt: datetime; endAt: datetime
  class Config: from_attributes = True
  
class EventPage(BaseModel):
  items: list[EventOut]
