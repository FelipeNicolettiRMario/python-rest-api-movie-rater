from typing import List
import uuid
from models.base import Base

class BaseService:

    def __init__(self, session) -> None:
        self.session = session

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

    def _update_entity(self, values_input, entity):

        for key, value in values_input.dict().items():
            if value and entity.__getattribute__(key):
                entity.__setattr__(key,value)

        return entity

    def update_entity_by_id(self,entity,passed_uuid, values_input):

        entity_from_uuid = self.session.get(entity, uuid.UUID(passed_uuid))
        updated_entity = self._update_entity(values_input,entity_from_uuid)
        self.update(updated_entity)

    def delete_entity_from_uuid(self, entity, passed_uuid):
        entity_from_uuid = self.session.get(entity, passed_uuid)
        self.delete(entity_from_uuid)

    def get_all_from_entity(self, max_items: int, entity, layout_templates):

        entitys = self.session.query(entity).limit(max_items).all()
        return [layout_templates().dump(entity) for entity in entitys]
    