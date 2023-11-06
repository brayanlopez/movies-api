from pydantic import BaseModel, Field
from typing import Optional
import datetime


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year)
    rating: float = Field(default=10, ge=1, le=10)
    category: str = Field(default='Categoría', min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                'year': datetime.date.today().year,
                "rating": 9.8,
                "category": "Acción"
            }
        }
