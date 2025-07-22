from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class StatsHistory(BaseModel):
    area_id: UUID
    updated_at: datetime  # Changed from timestamp to match Counter model
    in_count: int
    out_count: int

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy objects

class StatsLive(BaseModel):
    area_id: UUID
    in_count: int
    out_count: int
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy objects
