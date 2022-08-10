import uuid
from marshmallow import post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pydantic import BaseModel

class ReviewInput(BaseModel):

    title: str
    stars: int
    text: str
    user_id: str
    movie_id: str

class ReviewReturnPayloadSimplified(SQLAlchemyAutoSchema):
    
    @post_dump
    def clean_id_field(self,data,**kwargs):
        data["id"] = uuid.UUID(data["id"]).hex
        return data