from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class ActivityCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str = Field(min_length=1, max_length=20)
    
class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    created_at: datetime
    
class TimeEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    activity_id: int
    started_at: datetime
    ended_at: Optional[datetime]