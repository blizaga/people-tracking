from sqlalchemy import Column, BigInteger, ForeignKey, String, JSON, TIMESTAMP, Boolean
from app.core.database import Base
from sqlalchemy.sql import func

class Detection(Base):
    __tablename__ = "detections"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tracking_id = Column(String, nullable=False)
    area_id = Column(ForeignKey("areas.id", ondelete="CASCADE"))
    frame_time = Column(TIMESTAMP(timezone=True), nullable=False)
    bbox = Column(JSON, nullable=False)
    entered = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
