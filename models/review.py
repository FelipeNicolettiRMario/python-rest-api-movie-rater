import uuid
from sqlalchemy import Column, ForeignKey, String, SmallInteger, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base
from models.movie import Movie
from models.user import User

class Review(Base):

    __tablename__ = "REV_REVIEW"

    id = Column("REV_ID",UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    title = Column("REV_TITLE", String(30),nullable=False)
    stars = Column("REV_STARS", SmallInteger,nullable=False)
    text = Column("REV_TEXT", String(4000),nullable=False)
    likes = Column("REV_LIKES", SmallInteger,nullable=False, default=0)
    unlikes = Column("REV_UNLIKES", SmallInteger,nullable=False, default=0)
    user_id = Column("REV_USU_ID",UUID(as_uuid=True),ForeignKey(User.id),nullable=False)
    movie_id = Column("REV_MOV_ID",UUID(as_uuid=True),ForeignKey(Movie.id),nullable=False)

    user = relationship("User",backref="User.reviews")
    movie = relationship("Movie",backref="Movie.reviews")

    __table_args__ = (
        UniqueConstraint(user_id,movie_id),
        CheckConstraint("REV_STARS <= 5",name="VALID_REV_STARS_VALUE")
    )

