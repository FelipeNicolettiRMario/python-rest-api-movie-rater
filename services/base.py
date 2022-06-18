from typing import List
from utils.session_manager import SessionManager
from models.base import Base

class BaseService:

    def __init__(self) -> None:
        self.session = SessionManager().get_session()

    def save_without_commit(self, entity: Base):
        self.session.add(entity)
        self.session.flush()
    def save_with_commit(self, entity: Base):

        self.session.add(entity)
        self.session.commit()

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
