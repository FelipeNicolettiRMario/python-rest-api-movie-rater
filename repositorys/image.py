import base64
import os
from typing import Any
from models.image import Image
from repositorys.i_base import IBase
from repositorys.base import BaseRepository

from zope.interface import implementer

@implementer(IBase)
class ImageRepository(BaseRepository):

    def __init__(self,session,*args: Any, **kwargs: Any) -> None:
        super().__init__(session,*args, **kwargs)

    def _generate_unique_path_to_image(self, image_entity: Image) -> str:
        return f"{os.getenv('LOCAL_IMAGE_FOLDER')}{image_entity.id}.jpeg"


    def _save_image_locally(self,image_encoded_in_base_64: str, image_entity: Image):

        image_decoded_from_base64 = base64.b64decode(image_encoded_in_base_64)

        path_to_file = self._generate_unique_path_to_image(image_entity)

        with open(path_to_file,'wb') as file:
            file.write(image_decoded_from_base64)

    def save_image_entity(self,image_encoded_in_base_64: str,image_entity: Image):
        image_entity.path = ""
        self.save_without_commit(image_entity)
        self._session.refresh(image_entity)
        
        try:
            self._save_image_locally(image_encoded_in_base_64, image_entity)
            image_entity.path = self._generate_unique_path_to_image(image_entity)
            self.save_with_commit(image_entity)

        except Exception as error:
            self._session.rollback()
            raise error
