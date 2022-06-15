from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
import os

engine = create_engine(os.getenv("DATABASE_URL"))

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SessionManager(metaclass=SingletonMeta):

    def get_session(self):

        if not hasattr(self,"session"):
            self.session = Session(engine)
            
        return self.session



