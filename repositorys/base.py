from typing import Any, Dict, List
import uuid
from sqlalchemy.orm import Session
from zope.interface import implementer

from models.base import Base
from repositorys.interfaces.i_base import IBaseRepository

@implementer(IBaseRepository)
class BaseRepository:

    def __init__(self, _session) -> None:
        self._session:Session = _session

    def save_without_commit(self, entity: Base):
        self._session.add(entity)
        self._session.flush()

    def save_with_commit(self, entity: Base):

        try:
            self._session.add(entity)
            self._session.commit()
        except Exception as error:
            self._session.rollback()
            raise error
            
    def delete(self, entity: Base):

        self._session.delete(entity)
        self._session.commit()

    def update(self, entity: Base):

        self._session.merge(entity)
        self._session.commit()

    def save_batch_without_commit(self, entitys: List[Base]):

        self._session.add_all(entitys)

    def save_batch_with_commit(self, entitys: List[Base]):

        self._session.add_all(entitys)
        self._session.commit()

    def create_entity(self, entity: Base, dict_of_attributes: Dict[str,Any]):

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

        entity_from_uuid = self._session.get(entity,passed_id)
        updated_entity = self.update_entity(values_input,entity_from_uuid)
        self.update(updated_entity)

    def delete_entity_from_uuid(self, entity, passed_uuid):
        entity_from_uuid = self._session.get(entity, passed_uuid)
        self.delete(entity_from_uuid)

    def get_all_from_entity(self, max_items: int, entity, layout_templates):

        entitys = self._session.query(entity).limit(max_items).all()
        return [layout_templates().dump(entity) for entity in entitys]
    
    def get_entity_by_id(self, entity: Base, id) -> Base:
        return self._session.get(entity, id)
