import uuid
from zope.interface import Interface

from models.image import Image

class IImageService(Interface):

    def _create_image_entity(self, storage_type: str, image_type: str) -> Image:
        pass

    def create_and_save_image_entity(self,image_encoded_in_base_64: str, storage_type: str, image_type: str) -> Image:
        pass

    def update_image(self, image_encoded_in_base_64: str, image: Image):
        pass

    def delete_image(self, image_entity: Image):
        pass

    def delete_image_from_image_uuid(self, uuid: uuid.UUID):
        pass