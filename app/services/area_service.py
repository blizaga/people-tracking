import logging
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.area import Area

logger = logging.getLogger(__name__)

class AreaService:
    def __init__(self):
        self.active_areas_cache: Dict[str, Area] = {}
        self.default_area_id: Optional[str] = None
    
    def get_active_areas(self, session: Session) -> List[Area]:
        """Get all areas yang memiliki polygon"""
        return session.query(Area).filter(Area.polygon.isnot(None)).all()
    
    def get_default_area(self, session: Session) -> Optional[Area]:
        """Get area default (yang pertama tersedia atau yang ditandai sebagai default)"""
        # Prioritas 1: Area yang namanya mengandung 'default' atau 'main'
        default_area = session.query(Area).filter(
            Area.polygon.isnot(None),
            Area.name.ilike('%default%') | Area.name.ilike('%main%')
        ).first()
        
        if default_area:
            return default_area
            
        # Prioritas 2: Area pertama yang tersedia
        return session.query(Area).filter(Area.polygon.isnot(None)).first()
    
    def get_area_by_id(self, session: Session, area_id: str) -> Optional[Area]:
        """Get area by ID"""
        return session.query(Area).filter_by(id=area_id).first()
    
    def get_area_by_name(self, session: Session, name: str) -> Optional[Area]:
        """Get area by name"""
        return session.query(Area).filter_by(name=name).first()
    
    def set_default_area(self, area_id: str):
        """Set default area ID untuk detection"""
        self.default_area_id = area_id
        logger.info(f"Default area set to: {area_id}")
    
    def get_detection_areas(self, session: Session, area_id: Optional[str] = None) -> List[Area]:
        """
        Get areas untuk detection
        
        Args:
            area_id: Specific area ID, jika None akan menggunakan semua area aktif
        """
        if area_id:
            area = self.get_area_by_id(session, area_id)
            return [area] if area else []
        
        # Jika ada default area yang di-set
        if self.default_area_id:
            area = self.get_area_by_id(session, self.default_area_id)
            if area:
                return [area]
        
        # Fallback ke semua area aktif
        return self.get_active_areas(session)

# Global service instance
area_service = AreaService()
