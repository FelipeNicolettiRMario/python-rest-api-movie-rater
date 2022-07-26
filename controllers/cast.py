from fastapi import APIRouter, Depends, UploadFile, Form
from repositorys.cast import CastRepository

from services.cast import CastService

from utils.serializer.cast import CastInput, CastInputUpdate
from utils.session_manager import SessionManager

cast = APIRouter()

@cast.post("/cast/member")
async def create_cast_member(cast_member: CastInput,
                      dbSession = Depends(SessionManager().get_session)):
    
    cast_service = CastService(CastRepository(dbSession))
    return cast_service.add_cast_member_to_movie(cast_member)

@cast.put("/cast/member")
async def update_cast_member(cast_member: CastInputUpdate,
                            dbSession = Depends(SessionManager().get_session)):

    cast_service = CastService(CastRepository(dbSession))
    return cast_service.update_cast_member_from_movie(cast_member)
    
@cast.delete("/cast/member")
async def delete_cast_member(cast_member: CastInput,
                            dbSession = Depends(SessionManager().get_session)):
    
    cast_service = CastService(CastRepository(dbSession))
    return cast_service.remove_cast_member_from_movie(cast_member)

@cast.get("/cast/movie/{movie_uuid}")
async def get_cast_from_movie(movie_uuid:str,
                              dbSession = Depends(SessionManager().get_session)):

    cast_service = CastService(CastRepository(dbSession))
    return cast_service.get_cast_from_movie(movie_uuid)