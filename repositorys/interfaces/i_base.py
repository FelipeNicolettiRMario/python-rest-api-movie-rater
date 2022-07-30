from typing import Any, Dict, List
from zope.interface import Interface, Attribute

from sqlalchemy.orm import Session

from models.base import Base

class IBaseRepository(Interface):

    _session:Session = Attribute("Session for database Work")

    def save_without_commit(self, entity: Base):
        pass

    def save_with_commit(self, entity: Base):
        pass

    def delete(self, entity: Base):
        pass

    def update(self, entity: Base):
        pass

    def save_batch_without_commit(self, entitys: List[Base]):
        pass

    def save_batch_with_commit(self, entitys: List[Base]):
        pass
 
    def create_entity(self, entity: Base, dict_of_attributes: Dict[str,Any]):
        pass
    
    def update_entity(self, values_input, entity):
        pass

    def update_entity_by_id(self,entity,passed_id, values_input):
        pass

    def delete_entity_from_uuid(self, entity, passed_uuid):
        pass

    def get_all_from_entity(self, max_items: int, entity, layout_templates):
        pass

    def get_entity_by_id(self, entity: Base, id) -> Base:
        pass
    