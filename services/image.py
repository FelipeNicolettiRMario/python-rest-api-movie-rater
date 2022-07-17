import uuid
from models.image import E_IMAGE_TYPE, E_MEDIA_STORAGE_TYPE, Image
import base64
import os
from services.base import BaseService

class ImageService(BaseService):

    def __init__(self, session) -> None:
        super().__init__(session)

    def _generate_image_settings(self,image_encoded_in_base64: str) -> Dict[str,str]:
        return {
            "image_encoded_in_base64":image_encoded_in_base64,
            "storage_type": E_MEDIA_STORAGE_TYPE.LOCAL.value,
            "image_type": E_IMAGE_TYPE.PROFILE.value
        } if image_encoded_in_base64 else None


    def _create_image_entity(self, storage_type: str, image_type: str) -> Image:
        image = Image()
        image.storage_type = storage_type
        image.image_type = image_type

        return image

    def _generate_unique_path_to_image(self, image_entity: Image) -> str:
        return f"{os.getenv('LOCAL_IMAGE_FOLDER')}{image_entity.id}.jpeg"

    def _save_image_entity(self,image_encoded_in_base_64: str,image_entity: Image):
        image_entity.path = ""
        self.save_without_commit(image_entity)
        self.session.refresh(image_entity)
        
        try:
            self._save_image_locally(image_encoded_in_base_64, image_entity)
            image_entity.path = self._generate_unique_path_to_image(image_entity)
            self.save_with_commit(image_entity)

        except Exception as error:
            self.session.rollback()
            raise error

    def _save_image_locally(self,image_encoded_in_base_64: str, image_entity: Image):

        image_decoded_from_base64 = base64.b64decode(image_encoded_in_base_64)

        path_to_file = self._generate_unique_path_to_image(image_entity)

        with open(path_to_file,'wb') as file:
            file.write(image_decoded_from_base64)

    def create_and_save_image_entity(self,image_encoded_in_base_64: str, storage_type: str, image_type: str) -> Image:

        image = self._create_image_entity(storage_type, image_type)
        self._save_image_entity(image_encoded_in_base_64, image)

        return image

    def update_image(self, image_encoded_in_base_64: str, image: Image):

        self._save_image_locally(image_encoded_in_base_64, image)
        
        image.path = self._generate_unique_path_to_image(image)
        self.update(image)

    def delete_image(self, image_entity: Image):

        path_of_image = self._generate_unique_path_to_image(image_entity)

        try:
            os.remove(path_of_image)
            self.delete(image_entity)

        except Exception as error:
            raise error

    def delete_image_from_image_uuid(self, uuid: uuid.UUID):

        image_to_delete = self.session.get(Image, uuid)

        if image_to_delete:

            self.delete_image(image_to_delete)