from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.config_polygon import PolygonAreaConfig, AreaConfigResponse
from app.models.area import Area
import uuid

router = APIRouter()

@router.post("/api/config/area", response_model=AreaConfigResponse)
def set_area(config: PolygonAreaConfig, db: Session = Depends(get_db)):
    """
    Set or update area configuration with polygon and name.
    
    **Dynamic area_id behavior:**
    - If area_id is provided: updates existing or creates with that ID
    - If area_id is not provided: generates new UUID and creates new area
    
    **Use cases:**
    1. Create new area with auto-generated ID (don't provide area_id)
    2. Update existing area (provide existing area_id)
    3. Create area with specific ID (provide new area_id)
    """
    # Generate UUID jika area_id tidak diberikan
    if not config.area_id:
        config.area_id = str(uuid.uuid4())
        # Buat area baru dengan UUID yang di-generate
        area = Area(id=config.area_id, name=config.name, polygon=config.polygon)
        db.add(area)
    else:
        # Cari area berdasarkan area_id yang diberikan
        area = db.query(Area).filter_by(id=config.area_id).first()
        if not area:
            # Buat baru dengan area_id yang diberikan
            area = Area(id=config.area_id, name=config.name, polygon=config.polygon)
            db.add(area)
        else:
            # Update area yang sudah ada
            area.name = config.name
            area.polygon = config.polygon
    
    db.commit()
    return {
        "status": "ok", 
        "area_id": config.area_id,
        "message": "Area created/updated successfully"
    }
