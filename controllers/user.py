from services.user import UserService
from fastapi import APIRouter, File, UploadFile, Form
import json
from base64 import b64encode

from utils.serializer.user import UserInput

user = APIRouter()

@user.post("/user")
async def create_user(params = Form(...), image: UploadFile = File(...)):

    user_service = UserService()
    user = UserInput(**json.loads(params))
    image_content = await image.read()

    return user_service.save_user(user, b64encode(image_content).decode("UTF-8"))