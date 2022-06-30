from models.image import Image
import base64
import os
from services.base import BaseService

class ImageService(BaseService):

    def __init__(self) -> None:
        super().__init__()

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

    def update_image(self, image_encoded_in_base_64: str, image_uuid: str):

        self._save_image_locally(image_encoded_in_base_64, image_uuid)
        
        image_entity = self.session.query(Image, image_entity)
        image_entity.path = self._generate_unique_path_to_image(image_entity)
        self.update(image_entity)

    def delete_image(self, image_entity: Image):

        path_of_image = self._generate_unique_path_to_image(image_entity)

        try:
            os.remove(path_of_image)
            self.delete(image_entity)

        except Exception as error:
            raise error

        