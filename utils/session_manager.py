from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
import os

engine = create_engine(os.getenv("DATABASE_URL"))

class SessionManager:

    def get_session(self):

        session = Session(engine)
            
        return session



