import uuid
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base
from models.movie import Movie
from models.participant import Participant

class Cast(Base):

    __tablename__ = "CAS_CAST"

    movie_id = Column("CAS_MOV_ID",UUID(as_uuid=True),ForeignKey(Movie.id),nullable=False)
    participant_id = Column("CAS_PAR_PARTICIPANT",UUID(as_uuid=True),ForeignKey(Participant.id),default=uuid.uuid4,nullable=False)
    character = Column("CAS_CHARACTER", String(100),nullable=False)

    participant = relationship("Participant",backref="Participant.movies")
    movie = relationship("Movie",backref="Movie.cast")

    __table_args__ = (
        PrimaryKeyConstraint(movie_id,participant_id,character),
    )


