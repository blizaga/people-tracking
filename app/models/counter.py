from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP, Integer
from sqlalchemy.sql import func
from app.core.database import Base

class Counter(Base):
    __tablename__ = "counters"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    area_id = Column(ForeignKey("areas.id", ondelete="CASCADE"), unique=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    in_count = Column(Integer, default=0)
    out_count = Column(Integer, default=0)
