from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import ActivityCreate, ActivityRead
from app.models import Activity


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