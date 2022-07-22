from typing import Dict, List
from fastapi.responses import JSONResponse
import uuid

from models.cast import Cast
from models.movie import Movie
from models.participant import Participant
from services.base import BaseService
from utils.response import create_response

from utils.serializer.cast import CastInput, CastInputUpdate, CastReturnPayloadSimplified



class CastService(BaseService):

    def __init__(self, session) -> None:
        super().__init__(session)

    def add_cast_member_to_movie(self,cast_input: CastInput)->JSONResponse:

        movie = self.session.get(Movie,cast_input.movie_id)
        participant = self.session.get(Participant,cast_input.participant_id)

        if movie and participant:

            cast = self._create_entity(Cast, cast_input.dict())
            self.save_with_commit(cast)
            return create_response(body={"detail":"Character added to movie"})
        
        return create_response(500, body={"detail":"Movie or participant not exists"})

    def remove_cast_member_from_movie(self, cast_input: CastInput)->JSONResponse:

        self.delete_entity_from_uuid(Cast,(uuid.UUID(cast_input.movie_id), 
                                       uuid.UUID(cast_input.participant_id),
                                       cast_input.character))

        return create_response(200, {"detail":"Cast member deleted with success"})

    def update_cast_member_from_movie(self, cast_input: CastInputUpdate)->JSONResponse:

        self.update_entity_by_id(Cast,(uuid.UUID(cast_input.input_original_value.movie_id), 
                                       uuid.UUID(cast_input.input_original_value.participant_id),
                                       cast_input.input_original_value.character),cast_input)

        return create_response(200,{"detail":"Cast updated with success"})

    def get_cast_from_movie(self, movie_uuid: str)-> List[Cast]:

        cast_members = self.session.query(Cast).filter(Cast.movie_id == uuid.UUID(movie_uuid)).all()

        return create_response(200, body={"cast_members":[cast_member.character for cast_member in cast_members]})