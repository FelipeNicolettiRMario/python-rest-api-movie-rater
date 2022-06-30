from services.user import UserService
from fastapi import APIRouter, Depends, File, UploadFile, Form
import json
from base64 import b64encode

from utils.serializer.general import SearchStandardQueryString
from utils.serializer.user import UserInput

user = APIRouter()

@user.post("/user")
async def create_user(params = Form(...), image: UploadFile = File(...)):

    user_service = UserService()
    user = UserInput(**json.loads(params))
    image_content = await image.read()

    return user_service.save_user(user, b64encode(image_content).decode("UTF-8"))

@user.get("/user")
async def get_all_users(pagination_info: SearchStandardQueryString = Depends()):
    user_service = UserService()
    return user_service.get_all_users(pagination_info.max_items)