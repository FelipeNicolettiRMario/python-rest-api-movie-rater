from zope.interface import Interface

from models.image import Image

class IImageRepository(Interface):
    def _generate_unique_path_to_image(self, image_entity: Image) -> str:
        pass

    def _save_image_locally(self,image_encoded_in_base_64: str, image_entity: Image):
        pass

    def save_image_entity(self,image_encoded_in_base_64: str,image_entity: Image):
        pass