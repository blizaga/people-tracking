from sqlalchemy import Column, String, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from sqlalchemy.sql import func

class Area(Base):
    __tablename__ = "areas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    coordinates = Column(JSON, nullable=False)  # Legacy field
    polygon = Column(JSON, nullable=True)       # New field for polygon coordinates
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    @property
    def polygon_coordinates(self):
        """Get polygon coordinates, fallback to coordinates if polygon is None"""
        return self.polygon if self.polygon is not None else self.coordinates
