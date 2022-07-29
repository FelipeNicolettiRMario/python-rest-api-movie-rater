from typing import List
from fastapi.responses import JSONResponse
import uuid
from zope.interface import implementer

from models.cast import Cast
from models.movie import Movie
from models.participant import Participant

from services.base import BaseService
from services.interfaces.i_base import IBase
from services.interfaces.i_cast import ICastService

from utils.response import create_response

from utils.serializer.cast import CastInput, CastInputUpdate


@implementer(IBase)
@implementer(ICastService)
class CastService(BaseService):

    def __init__(self, repository) -> None:
        super().__init__(repository)

    def add_cast_member_to_movie(self,cast_input: CastInput)->JSONResponse:

        movie = self.repository.get_entity_by_id(Movie,cast_input.movie_id)
        participant = self.repository.get_entity_by_id(Participant,cast_input.participant_id)

        if movie and participant:

            cast = self.repository.create_entity(Cast, cast_input.dict())
            self.repository.save_with_commit(cast)
            return create_response(body={"detail":"Character added to movie"})
        
        return create_response(500, body={"detail":"Movie or participant not exists"})

    def remove_cast_member_from_movie(self, cast_input: CastInput)->JSONResponse:

        self.repository.delete_entity_from_uuid(Cast,(uuid.UUID(cast_input.movie_id), 
                                       uuid.UUID(cast_input.participant_id),
                                       cast_input.character))

        return create_response(200, {"detail":"Cast member deleted with success"})

    def update_cast_member_from_movie(self, cast_input: CastInputUpdate)->JSONResponse:

        self.repository.update_entity_by_id(Cast,(uuid.UUID(cast_input.input_original_value.movie_id), 
                                       uuid.UUID(cast_input.input_original_value.participant_id),
                                       cast_input.input_original_value.character),cast_input)

        return create_response(200,{"detail":"Cast updated with success"})

    def get_cast_from_movie(self, movie_uuid: str)-> List[Cast]:

        cast_members = self.repository.get_cast_from_movie(movie_uuid)

        return create_response(200, body={"cast_members":[cast_member.character for cast_member in cast_members]})