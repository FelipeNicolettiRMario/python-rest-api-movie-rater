from typing import Dict
from hashlib import sha256
from uuid import UUID
import uuid
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from zope.interface import implementer

from models.base import Base
from models.image import E_IMAGE_TYPE, E_MEDIA_STORAGE_TYPE
from models.user import User

from services.image import ImageService
from services.new_base import BaseService, IBase

from utils.serializer.user import UserInput, UserInputUpdate, UserReturnPayloadSimplified
from utils.response import create_response

from repositorys.image import ImageRepository

@implementer(IBase)
class UserService(BaseService):

    def __init__(self, repository) -> None:
        super().__init__(repository)
        self.image_service = ImageService(self.repository.create_repository_with_same_session(ImageRepository))
    
    def _save_user(self, user_entity: Base,image_settings: Dict[str,str] = None):

        if image_settings:
            image = self.image_service.create_and_save_image_entity(image_settings.get("image_encoded_in_base64"),
                                                                    image_settings.get("storage_type"),
                                                                    image_settings.get("image_type")
                                                                    )
            user_entity.profile_image_id = image.id

        self.repository.save_with_commit(user_entity)
    

    def _generate_password_hash(self, password: str) -> str:
        return sha256(password.encode("UTF-8")).hexdigest()

    def save_user(self, user_input: UserInput, image_encoded_in_base64: str = None) -> JSONResponse:

        user = self.repository.create_entity(User,user_input.dict())

        try:
            self._save_user(user,self.image_service._generate_image_settings(image_encoded_in_base64,
                                                                             E_MEDIA_STORAGE_TYPE.LOCAL,
                                                                             E_IMAGE_TYPE.PROFILE))
        
        except (IntegrityError,UniqueViolation,PendingRollbackError) as error:
            
            if user.profile_image_id:
                self.image_service.delete_image_from_image_uuid(user.profile_image_id)

            if isinstance(error,IntegrityError):
                detail = "Email could not be duplicated"
            else:
                detail = "Internal Error"
            print(error)

            return create_response(500, {"error":"Error on try to save user","detail":detail})

        return create_response(201, UserReturnPayloadSimplified().dump(user))

    def update_user(self, passed_uuid: UUID, user_input: UserInputUpdate):

        self.repository.update_entity_by_id(User, passed_uuid,user_input)
        return create_response(200, {"message":"User updated with success"})

    def update_profile_picture(self, passed_uuid: UUID, image_encoded_in_base64: str = None):
        
        user_from_uuid = self.repository.get_entity_by_id(User, uuid.UUID(passed_uuid))
        self.image_service.update_image(image_encoded_in_base64, user_from_uuid.profile_image)

        return create_response(200, {"message":"Profile picture updated with success"})
    
    def delete_user(self, passed_uuid: str):

        try:
            self.repository.delete_entity_from_uuid(User,passed_uuid)
            return create_response(200, {"message":"User deleted with success"})

        except IntegrityError:
            return create_response(500, {"error":"Error on try to delete user"})

    def get_all_users(self,max_items: int):
        return self.repository.get_all_from_entity(max_items, User, UserReturnPayloadSimplified)