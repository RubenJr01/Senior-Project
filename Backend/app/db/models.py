from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  name = Column(String, nullable=True)
  events = relationship("Event", back_populates="owner", cascade="all,delete")
  
class Event(Base):
  __tablename__ = "events"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  start_at = Column(DateTime, nullable=False)
  end_at = Column(DateTime, nullable=False)
  owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
  owner = relationship("User", back_populates="events")