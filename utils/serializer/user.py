from datetime import datetime
from typing import Optional
import uuid
from marshmallow import post_dump
from pydantic import BaseModel
from models.user import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class UserInput(BaseModel):

    name: str
    password: str 
    email: str
    description: Optional[str]
    birthday: str

class UserInputUpdate(BaseModel):

    name: Optional[str]
    password: Optional[str] 
    email: Optional[str]
    description: Optional[str]
    birthday: Optional[datetime]

class UserReturnPayloadSimplified(SQLAlchemyAutoSchema):
    
    @post_dump
    def clean_id_field(self,data,**kwargs):
        data["id"] = uuid.UUID(data["id"]).hex
        return data

    class Meta:
        model = User
        load_instance = True
        exclude=("password",)
    
