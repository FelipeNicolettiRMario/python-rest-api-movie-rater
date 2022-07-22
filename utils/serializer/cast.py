from typing import Optional
from marshmallow import post_dump
from pydantic import BaseModel
from models.user import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class CastInput(BaseModel):

    movie_id: str
    participant_id: str 
    character: str

class CastInputUpdate(BaseModel):

    input_original_value: CastInput
    movie_id: Optional[str]
    participant_id: Optional[str] 
    character: Optional[str]

class CastReturnPayloadSimplified(SQLAlchemyAutoSchema):
    
    class Meta:
        model = User
        load_instance = True
        exclude=("CAS_MOV_ID","CAS_PAR_PARTICIPANT")

