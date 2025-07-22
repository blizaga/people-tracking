from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from uuid import UUID

class PolygonAreaConfig(BaseModel):
    area_id: Optional[str] = Field(
        None, 
        description="UUID of the area. If not provided, will be auto-generated",
        example="4aeb238c-be39-4c1b-8c9f-828669dddf62"
    )
    name: str = Field(
        ..., 
        description="Name of the area",
        example="Pedestrian Crossing Area"
    )
    polygon: List[Tuple[int, int]] = Field(
        ..., 
        description="List of polygon coordinates as [x, y] pairs",
        example=[[300, 400], [900, 400], [1000, 720], [200, 720]]
    )

    class Config:
        schema_extra = {
            "examples": {
                "with_area_id": {
                    "summary": "Update existing area with specific ID",
                    "description": "Update an existing area or create new one with specified area_id",
                    "value": {
                        "area_id": "4aeb238c-be39-4c1b-8c9f-828669dddf62",
                        "name": "Pedestrian Crossing Area",
                        "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
                    }
                },
                "without_area_id": {
                    "summary": "Create new area with auto-generated ID",
                    "description": "Create a new area with automatically generated UUID",
                    "value": {
                        "name": "New Crossing Area",
                        "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
                    }
                }
            }
        }

class AreaConfigResponse(BaseModel):
    status: str = Field(example="ok")
    area_id: str = Field(example="4aeb238c-be39-4c1b-8c9f-828669dddf62")
    message: str = Field(example="Area created/updated successfully")
