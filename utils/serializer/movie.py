from typing import Optional
import uuid
from marshmallow import post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pydantic import BaseModel, validator

from models.movie import Movie

class MovieInput(BaseModel):
    name: str
    year: int
    director_id: str
    studio: str


class MovieInputUpdate(BaseModel):
    name: Optional[str]
    year: Optional[int]
    director_id: Optional[str]
    studio: Optional[str]

class MovieReturnPayloadSimplified(SQLAlchemyAutoSchema):
    
    @post_dump
    def clean_id_field(self,data,**kwargs):
        data["id"] = uuid.UUID(data["id"]).hex
        return data

    class Meta:
        model = Movie
        load_instance = True    