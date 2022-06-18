from typing import Dict
from hashlib import sha256
from uuid import UUID
from models.base import Base
from models.user import User
from models.image import E_IMAGE_TYPE, E_MEDIA_STORAGE_TYPE, Image
from services.base import BaseService
from services.image import ImageService
from utils.serializer.user import UserInput, UserInputUpdate, UserReturnPayloadSimplified
from fastapi.responses import JSONResponse
from utils.response import create_response

class UserService(BaseService):

    def __init__(self) -> None:
        super().__init__()
        self.image_service = ImageService()

    def _generate_image_settings(self,image_encoded_in_base64: str) -> Dict[str,str]:
        return {
            "image_encoded_in_base64":image_encoded_in_base64,
            "storage_type": E_MEDIA_STORAGE_TYPE.LOCAL.value,
            "image_type": E_IMAGE_TYPE.PROFILE.value
        } if image_encoded_in_base64 else None

    def _create_user_entity(self, user_input: UserInput, image_settings: Dict[str,str] = None) -> User:

        user = User()
        user.name = user_input.name
        user.email = user_input.email
        user.birthday = user_input.birthday
        user.password = self._generate_password_hash(user_input.password)
        user.description = user_input.description

        if image_settings:
            image = self.image_service.create_and_save_image_entity(image_settings.get("image_encoded_in_base64"),
                                                                    image_settings.get("storage_type"),
                                                                    image_settings.get("image_type")
                                                                    )
            user.profile_image_id = image.id

        return user
    
    def _save_user(self, user_entity: Base):

        self.save_with_commit(user_entity)

    def _generate_password_hash(self, password: str) -> str:
        return sha256(password.encode("UTF-8")).hexdigest()

    def save_user(self, user_input: UserInput, image_encoded_in_base64: str = None) -> JSONResponse:

        user = self._create_user_entity(user_input, self._generate_image_settings(image_encoded_in_base64))
        self._save_user(user)

        return create_response(201, UserReturnPayloadSimplified().dump(user))

    def _update_user_entity(self, user_input: UserInputUpdate, user: User) -> User:

        for key, value in user_input.dict().items():

            if value and user.__getattribute__(key):
                user.__setattr__(key,value)

        return user

    def update_user(self, uuid: UUID, user_input: UserInputUpdate):

        user_from_uuid = self.session.get(User,uuid)
        self._update_user_entity(user_input, user_from_uuid)
        return create_response()

    def update_profile_picture(self, uuid: UUID, image_encoded_in_base64: str = None):
        
        user_from_uuid = self.session.get(User, uuid)
        
        self.image_service.update_image(image_encoded_in_base64, user_from_uuid.profile_image)

        return create_response()

    