from typing import Dict
from hashlib import sha256
from uuid import UUID
import uuid

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError
from models.base import Base
from models.user import User
from services.base import BaseService
from services.image import ImageService
from sqlalchemy.exc import IntegrityError
from utils.serializer.user import UserInput, UserInputUpdate, UserReturnPayloadSimplified
from fastapi.responses import JSONResponse
from utils.response import create_response

class UserService(BaseService):

    def __init__(self, session) -> None:
        super().__init__(session)
        self.image_service = ImageService(session)

    def _create_user_entity(self, user_input: UserInput) -> User:

        user = User()
        user.name = user_input.name
        user.email = user_input.email
        user.birthday = user_input.birthday
        user.password = self._generate_password_hash(user_input.password)
        user.description = user_input.description

        return user
    
    def _save_user(self, user_entity: Base,image_settings: Dict[str,str] = None):

        if image_settings:
            image = self.image_service.create_and_save_image_entity(image_settings.get("image_encoded_in_base64"),
                                                                    image_settings.get("storage_type"),
                                                                    image_settings.get("image_type")
                                                                    )
            user_entity.profile_image_id = image.id

        self.save_with_commit(user_entity)
    

    def _generate_password_hash(self, password: str) -> str:
        return sha256(password.encode("UTF-8")).hexdigest()

    def save_user(self, user_input: UserInput, image_encoded_in_base64: str = None) -> JSONResponse:

        user = self._create_user_entity(user_input)

        try:
            self._save_user(user,self._generate_image_settings(image_encoded_in_base64))
        
        except (IntegrityError,UniqueViolation,PendingRollbackError) as error:
            
            if user.profile_image_id:
                self.image_service.delete_image_from_image_uuid(user.profile_image_id)

            if isinstance(error,IntegrityError):
                detail = "Email could not be duplicated"
            else:
                detail = "Internal Error"

            return create_response(500, {"error":"Error on try to save user","detail":detail})

        return create_response(201, UserReturnPayloadSimplified().dump(user))

    def _update_user_entity(self, user_input: UserInputUpdate, user: User) -> User:

        for key, value in user_input.dict().items():
            if value and user.__getattribute__(key):
                user.__setattr__(key,value)

        return user

    def update_user(self, passed_uuid: UUID, user_input: UserInputUpdate):

        user_from_uuid = self.session.get(User,uuid.UUID(passed_uuid))
        updated_user = self._update_user_entity(user_input, user_from_uuid)
        self.update(updated_user)
        return create_response(200, {"message":"User updated with success"})

    def update_profile_picture(self, passed_uuid: UUID, image_encoded_in_base64: str = None):
        
        user_from_uuid = self.session.get(User, uuid.UUID(passed_uuid))
        self.image_service.update_image(image_encoded_in_base64, user_from_uuid.profile_image)

        return create_response(200, {"message":"Profile picture updated with success"})
    
    def delete_user(self, passed_uuid: str):

        try:
            user_from_uuid = self.session.get(User, uuid.UUID(passed_uuid))
            self.delete(user_from_uuid)
            return create_response(200, {"message":"User deleted with success"})

        except IntegrityError:
            return create_response(500, {"error":"Error on try to delete user"})

    def get_all_users(self,max_items: int):

        users = self.session.query(User).limit(max_items).all()
        return [UserReturnPayloadSimplified().dump(user) for user in users]