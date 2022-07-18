from base64 import b64encode
import json
from fastapi import APIRouter, Depends, UploadFile, Form

from services.participant import ParticipantService
from utils.serializer.general import SearchStandardQueryString
from utils.session_manager import SessionManager
from utils.serializer.participant import ParticipantInput, ParticipantInputUpdate

participant = APIRouter()

@participant.post("/participant")
async def create_participant(image: UploadFile,
                      params = Form(...),
                      dbSession = Depends(SessionManager().get_session)):
    
    participant_service = ParticipantService(dbSession)
    participant = ParticipantInput(**json.loads(params))
    image_content = await image.read()

    return participant_service.save_participant(participant, b64encode(image_content).decode("UTF-8"))

@participant.get("/participant")
async def get_all_participants(pagination_info: SearchStandardQueryString = Depends(),
                        dbSession = Depends(SessionManager().get_session)):

    participant_service = ParticipantService(dbSession)
    return participant_service.get_all_participants(pagination_info.max_items)

@participant.delete("/participant/{uuid}")
async def delete_participant(uuid: str,
                     dbSession = Depends(SessionManager().get_session)):

    participant_service = ParticipantService(dbSession)
    return participant_service.delete_participant(uuid)

@participant.put("/participant/{uuid}")
async def update_participant(uuid: str, 
                     new_information: ParticipantInputUpdate,
                     dbSession = Depends(SessionManager().get_session)):

    participant_service = ParticipantService(dbSession)
    return participant_service.update_participant(uuid,new_information)

@participant.put("/participant/image/{uuid}")
async def update_participant_image(image: UploadFile,
                            uuid:str,
                            dbSession = Depends(SessionManager().get_session)):

    participant_service = ParticipantService(dbSession)
    image_content = await image.read()
    return participant_service.update_participant_picture(uuid,b64encode(image_content).decode("UTF-8"))