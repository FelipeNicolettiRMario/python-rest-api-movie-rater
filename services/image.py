from typing import Dict
import uuid
import os

from zope.interface import implementer

from models.image import Image
from services.base import BaseService
from services.interfaces.i_base import IBase
from services.interfaces.i_image import IImageService

@implementer(IImageService)
@implementer(IBase)
class ImageService(BaseService):

    def __init__(self, repository) -> None:
        super().__init__(repository)

    def _generate_image_settings(self,
                            image_encoded_in_base64: str,
                            storage_type,
                            image_type) -> Dict[str,str]:

        return {
            "image_encoded_in_base64":image_encoded_in_base64,
            "storage_type": storage_type.value,
            "image_type": image_type.value
        } if image_encoded_in_base64 else None


    def _create_image_entity(self, storage_type: str, image_type: str) -> Image:
        image = Image()
        image.storage_type = storage_type
        image.image_type = image_type

        return image

    def create_and_save_image_entity(self,image_encoded_in_base_64: str, storage_type: str, image_type: str) -> Image:

        image = self._create_image_entity(storage_type, image_type)
        self.repository.save_image_entity(image_encoded_in_base_64, image)

        return image

    def update_image(self, image_encoded_in_base_64: str, image: Image):

        self.repository._save_image_locally(image_encoded_in_base_64, image)
        
        image.path = self.repository._generate_unique_path_to_image(image)
        self.repository.update(image)

    def delete_image(self, image_entity: Image):

        path_of_image = self.repository._generate_unique_path_to_image(image_entity)

        try:
            os.remove(path_of_image)
            self.repository.delete(image_entity)

        except Exception as error:
            raise error

    def delete_image_from_image_uuid(self, uuid: uuid.UUID):

        image_to_delete = self.repository.get_entity_by_id(Image, uuid)

        if image_to_delete:

            self.delete_image(image_to_delete)