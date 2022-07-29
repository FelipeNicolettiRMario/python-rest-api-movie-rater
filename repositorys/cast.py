import base64
import os
from typing import Any, List
import uuid
from models.cast import Cast

from repositorys.interfaces.i_base import IBase
from repositorys.interfaces.i_cast import ICastRepository
from repositorys.base import BaseRepository

from zope.interface import implementer


@implementer(IBase)
@implementer(ICastRepository)
class CastRepository(BaseRepository):

    def __init__(self,session) -> None:
        super().__init__(session)

    def get_cast_from_movie(self, movie_uuid: str)-> List[Cast]:
        return self._session.query(Cast).filter(Cast.movie_id == uuid.UUID(movie_uuid)).all()