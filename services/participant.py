

from typing import Dict
from uuid import UUID
import uuid

from psycopg2 import IntegrityError
from models.image import E_IMAGE_TYPE, E_MEDIA_STORAGE_TYPE
from models.participant import Participant
from services.base import BaseService
from services.image import ImageService
from utils.response import create_response
from utils.serializer.participant import ParticipantInput, ParticipantInputUpdate, ParticipantReturnPayloadSimplified
from fastapi.responses import JSONResponse


class ParticipantService(BaseService):

    def __init__(self, session) -> None:
        super().__init__(session)
        self.image_service = ImageService(session)

    def _create_participant_entity(self,participant_input: ParticipantInput):

        participant = Participant()
        participant.name = participant_input.name
        participant.origin_country = participant_input.origin_country
        participant.description = participant_input.description

        return participant

    def _save_participant(self,participant_entity: Participant,image_settings: Dict[str,str] = None):
        if image_settings:
            image = self.image_service.create_and_save_image_entity(image_settings.get("image_encoded_in_base64"),
                                                                    image_settings.get("storage_type"),
                                                                    image_settings.get("image_type")
                                                                    )
            participant_entity.participant_image_id = image.id

        self.save_with_commit(participant_entity)

    def save_participant(self, participant_input: ParticipantInput, image_encoded_in_base64: str = None) -> JSONResponse:
        participant = self._create_participant_entity(participant_input)

        try:
            self._save_participant(participant,self.image_service._generate_image_settings(image_encoded_in_base64,
                                                                             E_MEDIA_STORAGE_TYPE.LOCAL,
                                                                             E_IMAGE_TYPE.PARTICIPANT))
    
        except (IntegrityError, Exception) as error:
            
            if participant.participant_image_id:
                self.image_service.delete_image_from_image_uuid(participant.participant_image_id)

            if isinstance(error,IntegrityError):
                detail = "Name could not be duplicated"
            else:
                detail = "Internal Error"

            return create_response(500, {"error":"Error on try to save participant","detail":detail})

        return create_response(201, ParticipantReturnPayloadSimplified().dump(participant))
    
    def update_participant(self, passed_uuid: UUID, participant_input: ParticipantInputUpdate):

        self.update_entity_by_id(Participant, passed_uuid,participant_input)
        return create_response(200, {"message":"Participant updated with success"})

    def update_participant_picture(self, passed_uuid: UUID, image_encoded_in_base64: str = None):
        
        participant_from_uuid = self.session.get(Participant, uuid.UUID(passed_uuid))
        self.image_service.update_image(image_encoded_in_base64, participant_from_uuid.participant_image)

        return create_response(200, {"message":"Participant picture updated with success"})

    def delete_participant(self, passed_uuid: str):

        try:
            self.delete_entity_from_uuid(Participant,passed_uuid)
            return create_response(200, {"message":"Participant deleted with success"})

        except:
            return create_response(500, {"error":"Error on try to delete participant"})
            
    def get_all_participants(self,max_items: int):
        return self.get_all_from_entity(max_items, Participant,ParticipantReturnPayloadSimplified)