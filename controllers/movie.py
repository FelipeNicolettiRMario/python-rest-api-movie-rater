from repositorys.interfaces.i_base import IBaseRepository
from repositorys.interfaces.i_image import IImageRepository
from services.interfaces.i_image import IImageService
from services.interfaces.i_movie import IMovieService
from fastapi import APIRouter, Depends, UploadFile, Form
import json
from base64 import b64encode
from utils.factory import Factory

from utils.serializer.general import SearchStandardQueryString
from utils.serializer.movie import MovieInput, MovieInputUpdate
from utils.session_manager import SessionManager

movie = APIRouter()

@movie.post("/movie")
async def create_movie(image: UploadFile,
                      params = Form(...),
                      dbSession = Depends(SessionManager().get_session)):
    
    service_factory = Factory()
    movie_service = service_factory.produce_service_with_repository_and_image_service(
        IBaseRepository,
        IMovieService,
        IImageService,
        IImageRepository,
        dbSession
    )    
    movie = MovieInput(**json.loads(params))
    image_content = await image.read()

    return movie_service.save_movie(movie, b64encode(image_content).decode("UTF-8"))

@movie.get("/movie")
async def get_all_movies(pagination_info: SearchStandardQueryString = Depends(),
                        dbSession = Depends(SessionManager().get_session)):

    service_factory = Factory()
    movie_service = service_factory.produce_service_with_repository_and_image_service(
        IBaseRepository,
        IMovieService,
        IImageService,
        IImageRepository,
        dbSession
    )    
    return movie_service.get_all_movies(pagination_info.max_items)

@movie.delete("/movie/{uuid}")
async def delete_movie(uuid: str,
                     dbSession = Depends(SessionManager().get_session)):

    service_factory = Factory()
    movie_service = service_factory.produce_service_with_repository_and_image_service(
        IBaseRepository,
        IMovieService,
        IImageService,
        IImageRepository,
        dbSession
    )    
    return movie_service.delete_movie(uuid)

@movie.put("/movie/{uuid}")
async def update_movie(uuid: str, 
                     new_information: MovieInputUpdate,
                     dbSession = Depends(SessionManager().get_session)):

    service_factory = Factory()
    movie_service = service_factory.produce_service_with_repository_and_image_service(
        IBaseRepository,
        IMovieService,
        IImageService,
        IImageRepository,
        dbSession
    )    
    return movie_service.update_movie(uuid,new_information)

@movie.put("/movie/image/{uuid}")
async def update_movie_image(image: UploadFile,
                            uuid:str,
                            dbSession = Depends(SessionManager().get_session)):

    service_factory = Factory()
    movie_service = service_factory.produce_service_with_repository_and_image_service(
        IBaseRepository,
        IMovieService,
        IImageService,
        IImageRepository,
        dbSession
    )    
    image_content = await image.read()
    return movie_service.update_profile_picture(uuid,b64encode(image_content).decode("UTF-8"))