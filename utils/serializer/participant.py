import uuid
from marshmallow import post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pydantic import BaseModel
from typing import Optional

from models.participant import Participant

class ParticipantInput(BaseModel):

    name: str
    origin_country: str
    description: Optional[str] = None

class ParticipantInputUpdate(BaseModel):

    name: Optional[str]
    origin_country: Optional[str]
    description: Optional[str]

class ParticipantReturnPayloadSimplified(SQLAlchemyAutoSchema):
    
    @post_dump
    def clean_id_field(self,data,**kwargs):
        data["id"] = uuid.UUID(data["id"]).hex
        return data

    class Meta:
        model = Participant
        load_instance = True