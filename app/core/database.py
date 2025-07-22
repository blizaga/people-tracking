from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_polygon(session, area_id: str):
    from app.models.area import Area  # Import here to avoid circular import
    area = session.query(Area).filter_by(id=area_id).first()
    if area:
        # Gunakan polygon jika ada, fallback ke coordinates
        return area.polygon_coordinates
    return None
