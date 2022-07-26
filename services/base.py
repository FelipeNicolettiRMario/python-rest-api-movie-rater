from typing import Any, Dict, List
import uuid
from sqlalchemy.orm import Session

from models.base import Base

class BaseService:

    def __init__(self, session) -> None:
        self.session:Session = session

    def save_without_commit(self, entity: Base):
        self.session.add(entity)
        self.session.flush()

    def save_with_commit(self, entity: Base):

        try:
            self.session.add(entity)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
            
    def delete(self, entity: Base):

        self.session.delete(entity)
        self.session.commit()

    def update(self, entity: Base):

        self.session.merge(entity)
        self.session.commit()

    def save_batch_without_commit(self, entitys: List[Base]):

        self.session.add_all(entitys)

    def save_batch_with_commit(self, entitys: List[Base]):

        self.session.add_all(entitys)
        self.session.commit()

    def _create_entity(self, entity: Base, dict_of_attributes: Dict[str,Any]):

        entity_initiated = entity()
        for key, value in dict_of_attributes.items():

            if hasattr(entity_initiated,key):
                entity_initiated.__setattr__(key,value)

        return entity_initiated

    def update_entity(self, values_input, entity):

        for key, value in values_input.dict().items():
            if value and hasattr(entity,key):
                entity.__setattr__(key,value)

        return entity

    def update_entity_by_id(self,entity,passed_id, values_input):
        
        if isinstance(passed_id, str):
            passed_id = uuid.UUID(passed_id)

        entity_from_uuid = self.session.get(entity,passed_id)
        updated_entity = self.update_entity(values_input,entity_from_uuid)
        self.update(updated_entity)

    def delete_entity_from_uuid(self, entity, passed_uuid):
        entity_from_uuid = self.session.get(entity, passed_uuid)
        self.delete(entity_from_uuid)

    def get_all_from_entity(self, max_items: int, entity, layout_templates):

        entitys = self.session.query(entity).limit(max_items).all()
        return [layout_templates().dump(entity) for entity in entitys]
    