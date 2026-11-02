from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import func, select, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated
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

@router.get("/activities", response_model=list[ActivityRead])
def list_activities(
    db: Session = Depends(get_db),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    stmt = select(Activity).offset(offset).limit(limit).order_by(Activity.id)
    
    activity_list = db.scalars(stmt).all()
    
    return activity_list

@router.get("/activities/{activity_id}", response_model=ActivityRead)
def find_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = db.get(Activity, activity_id)
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activité introuvable")
    
    return activity


@router.get("/activities/{activity_id}/entries", response_model=list[TimeEntryRead])
def get_activity_entries(
    activity_id: int,
    db: Session = Depends(get_db),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    activity = db.get(Activity, activity_id)
    
    if not activity:
        raise HTTPException(status_code=404, detail="Cette activité n'existe pas")

    stmt = select(TimeEntry).where(TimeEntry.activity_id==activity_id).order_by(TimeEntry.started_at.desc(), TimeEntry.id.desc()).offset(offset).limit(limit)
    entry_list = db.scalars(stmt).all()
    
    return entry_list
