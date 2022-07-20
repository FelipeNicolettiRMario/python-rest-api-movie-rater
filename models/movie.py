import uuid
from sqlalchemy import Column, ForeignKey, String, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base
from models.image import Image
from models.participant import Participant

class Movie(Base):

    __tablename__ = "MOV_MOVIE"

    id = Column("MOV_ID",UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    name = Column("MOV_NAME", String(50),nullable=False)
    year = Column("MOV_YEAR", SmallInteger,nullable=False)
    studio = Column("MOV_STUDIO",String,nullable=False)
    director_id = Column("MOV_DIRECTOR",UUID(as_uuid=True),ForeignKey(Participant.id),nullable=False)
    poster_id = Column("MOV_POSTER",UUID(as_uuid=True),ForeignKey(Image.id))

    director = relationship("Participant",backref="Participant.movies_directed")
    poster = relationship("Image")



