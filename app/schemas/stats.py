from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class StatsHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode for SQLAlchemy objects
    
    area_id: UUID
    updated_at: datetime  # Changed from timestamp to match Counter model
    in_count: int
    out_count: int

class StatsLive(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode for SQLAlchemy objects
    
    area_id: UUID
    in_count: int
    out_count: int
    updated_at: datetime
