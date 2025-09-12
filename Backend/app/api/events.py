from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.events import EventCreate, EventOut, EventPage
from app.db import models
router = APIRouter()

@router.get("", response_model=EventPage)
def list_events(db: Session = Depends(get_db), user=Depends(get_current_user)):
  rows = db.query(models.Event).filter_by(owner_id=user.id).order_by(models.Event.start_at).all()
  return {"items": [EventOut(id=r.id, title=r.title, startAt=r.start_at, endAt=r.end_at) for r in rows]}

@router.post("", status_code=201, response_model=EventOut)
def create_event(body: EventCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
  overlap = db.query(models.Event).filter(
    models.Event.owner_id==user.id,
    models.Event.start_at < body.endAt,
    models.Event.end_at > body.startAt
  ).first()
  if overlap:
    raise HTTPException(status_code=409, detail="Overlapping event")
  ev = models.Event(title=body.title, start_at=body.startAt, end_at=body.endAt, owner_id=user.id)
  db.add(ev); db.commit(); db.refresh(ev)
  return EventOut(id=ev.id, title=ev.title, startAt=ev.start_at, endAt=ev.end_at)
