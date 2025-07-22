from pydantic import BaseModel
from typing import List, Tuple
from uuid import UUID

class AreaConfigSchema(BaseModel):
    area_id: UUID
    name: str
    polygon: List[Tuple[int, int]]
