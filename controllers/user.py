from repositorys.image import ImageRepository
from services.image import ImageService
from services.user import UserService
from fastapi import APIRouter, Depends, UploadFile, Form
import json
from base64 import b64encode

from utils.serializer.general import SearchStandardQueryString
from utils.serializer.user import UserInput, UserInputUpdate
from utils.session_manager import SessionManager

from repositorys.base import BaseRepository

user = APIRouter()

@user.post("/user")
async def create_user(image: UploadFile,
                      params = Form(...),
                      dbSession = Depends(SessionManager().get_session)):
    
    user_service = UserService(BaseRepository(dbSession),ImageService(ImageRepository(dbSession)))
    user = UserInput(**json.loads(params))
    image_content = await image.read()

    return user_service.save_user(user, b64encode(image_content).decode("UTF-8"))

@user.get("/user")
async def get_all_users(pagination_info: SearchStandardQueryString = Depends(),
                        dbSession = Depends(SessionManager().get_session)):

    user_service = UserService(BaseRepository(dbSession),ImageService(ImageRepository(dbSession)))
    return user_service.get_all_users(pagination_info.max_items)

@user.delete("/user/{uuid}")
async def delete_user(uuid: str,
                     dbSession = Depends(SessionManager().get_session)):

    user_service = UserService(BaseRepository(dbSession),ImageService(ImageRepository(dbSession)))
    return user_service.delete_user(uuid)

@user.put("/user/{uuid}")
async def update_user(uuid: str, 
                     new_information: UserInputUpdate,
                     dbSession = Depends(SessionManager().get_session)):

    user_service = UserService(BaseRepository(dbSession),ImageService(ImageRepository(dbSession)))
    return user_service.update_user(uuid,new_information)

@user.put("/user/image/{uuid}")
async def update_user_image(image: UploadFile,
                            uuid:str,
                            dbSession = Depends(SessionManager().get_session)):

    user_service = UserService(BaseRepository(dbSession),ImageService(ImageRepository(dbSession)))
    image_content = await image.read()
    return user_service.update_profile_picture(uuid,b64encode(image_content).decode("UTF-8"))