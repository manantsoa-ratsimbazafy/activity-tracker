from sqlalchemy import Integer, String, DateTime, ForeignKey, Index
from sqlalchemy import func, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime
from typing import Optional, List
from app.db import Base

class Activity(Base):
    __tablename__="activity"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    time_entries: Mapped[List["TimeEntry"]] = relationship(back_populates="activity")
    
class TimeEntry(Base):
    __tablename__="time_entry"
    __table_args__= (
            Index("ix_activity_time_entry", "activity_id", unique=True, postgresql_where=text("ended_at IS NULL")),
        )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    activity: Mapped["Activity"] = relationship(back_populates="time_entries")