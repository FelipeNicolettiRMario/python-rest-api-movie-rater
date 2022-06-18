from datetime import datetime
from typing import Optional
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

    class Meta:
        model = User
        load_instance = True