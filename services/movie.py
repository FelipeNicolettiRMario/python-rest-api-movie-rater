from typing import Dict
from uuid import UUID
import uuid
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError

from models.base import Base
from models.image import E_IMAGE_TYPE, E_MEDIA_STORAGE_TYPE
from models.movie import Movie

from services.base import BaseService
from services.image import ImageService
from utils.response import create_response

from utils.serializer.movie import MovieInput, MovieInputUpdate, MovieReturnPayloadSimplified


class MovieService(BaseService):

    def __init__(self, session) -> None:
        super().__init__(session)
        self.image_service = ImageService(session)

    def _save_movie(self, movie_entity: Base,image_settings: Dict[str,str] = None):

        if image_settings:
            image = self.image_service.create_and_save_image_entity(image_settings.get("image_encoded_in_base64"),
                                                                    image_settings.get("storage_type"),
                                                                    image_settings.get("image_type")
                                                                    )
            movie_entity.poster_id = image.id

        self.save_with_commit(movie_entity)

    def save_movie(self, movie_input: MovieInput, image_encoded_in_base64: str = None) -> JSONResponse:

        movie = self._create_entity(Movie,movie_input.dict())

        try:
            self._save_movie(movie,self.image_service._generate_image_settings(image_encoded_in_base64,
                                                                             E_MEDIA_STORAGE_TYPE.LOCAL,
                                                                             E_IMAGE_TYPE.MOVIE))
        
        except (IntegrityError) as error:
            
            if movie.poster_id:
                self.image_service.delete_image_from_image_uuid(movie.poster_id)

            if isinstance(error,IntegrityError):
                detail = "Movie could not be duplicated"
            else:
                detail = "Internal Error"
            print(error)

            return create_response(500, {"error":"Error on try to save movie","detail":detail})

        return create_response(201, MovieReturnPayloadSimplified().dump(movie))

    def update_movie(self, passed_uuid: UUID, movie_input: MovieInputUpdate):

        self.update_entity_by_id(Movie, passed_uuid,movie_input)
        return create_response(200, {"message":"Movie updated with success"})

    def update_profile_picture(self, passed_uuid: UUID, image_encoded_in_base64: str = None):
        
        movie_from_uuid = self.session.get(Movie, uuid.UUID(passed_uuid))
        self.image_service.update_image(image_encoded_in_base64, movie_from_uuid.poster)

        return create_response(200, {"message":"Profile picture updated with success"})
    
    def delete_movie(self, passed_uuid: str):

        try:
            self.delete_entity_from_uuid(Movie,passed_uuid)
            return create_response(200, {"message":"Movie deleted with success"})

        except IntegrityError:
            return create_response(500, {"error":"Error on try to delete movie"})

    def get_all_movies(self,max_items: int):
        return self.get_all_from_entity(max_items, Movie, MovieReturnPayloadSimplified)