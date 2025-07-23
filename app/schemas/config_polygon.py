from pydantic import BaseModel, Field, ConfigDict
from typing import List, Tuple, Optional
from uuid import UUID

class PolygonAreaConfig(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "area_id": "4aeb238c-be39-4c1b-8c9f-828669dddf62",
                    "name": "Pedestrian Crossing Area",
                    "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
                },
                {
                    "name": "New Crossing Area",
                    "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
                }
            ]
        }
    )
    
    area_id: Optional[str] = Field(
        None, 
        description="UUID of the area. If not provided, will be auto-generated",
        examples=["4aeb238c-be39-4c1b-8c9f-828669dddf62"]
    )
    name: str = Field(
        ..., 
        description="Name of the area",
        examples=["Pedestrian Crossing Area"]
    )
    polygon: List[Tuple[int, int]] = Field(
        ..., 
        description="List of polygon coordinates as [x, y] pairs",
        examples=[[[300, 400], [900, 400], [1000, 720], [200, 720]]]
    )

class AreaConfigResponse(BaseModel):
    status: str = Field(examples=["ok"])
    area_id: str = Field(examples=["4aeb238c-be39-4c1b-8c9f-828669dddf62"])
    message: str = Field(examples=["Area created/updated successfully"])
