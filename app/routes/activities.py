from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import ActivityCreate, ActivityRead, TimeEntryRead
from app.models import Activity, TimeEntry


router = APIRouter()

@router.post("/activities", response_model=ActivityRead, status_code=201)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db)
):
    new_activity = Activity(name=activity.name)
    
    try:
        db.add(new_activity)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Activité déjà présente en base")
    
    db.refresh(new_activity)
    
    return new_activity

@router.post("/activities/{activity_id}/start", response_model=TimeEntryRead, status_code=201)
def start_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = db.get(Activity, activity_id)
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activité introuvable")
    
    begin = TimeEntry(activity_id=activity_id)
    
    try:
        db.add(begin)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Une session est déjà en cours")
    
    db.refresh(begin)
        
    return begin

@router.post("/activities/{activity_id}/stop", response_model=TimeEntryRead)
def stop_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = db.get(Activity, activity_id)
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activité introuvable")
    
    # stmt = statement
    stmt = select(TimeEntry).where(TimeEntry.activity_id==activity_id, TimeEntry.ended_at.is_(None))
    
    open_entry = db.scalars(stmt).one_or_none()
    
    if open_entry is None:
        raise HTTPException(status_code=404, detail="Aucune session ouverte pour cette activité")
    
    open_entry.ended_at=func.now()
    
    db.commit()
        
    db.refresh(open_entry)
        
    return open_entry