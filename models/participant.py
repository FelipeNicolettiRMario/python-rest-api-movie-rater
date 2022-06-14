from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base
from models.image import Image

class Participant(Base):

    __tablename__ = "PAR_PARTICIPANT"

    id = Column("PAR_ID",UUID(as_uuid=True),primary_key=True,nullable=False)
    name = Column("PAR_NAME", String(100),unique=True,nullable=False)
    origin_country = Column("PAR_ORIGIN_COUNTRY", String(100),nullable=False)
    description = Column("PAR_DESCRIPTION", String(100),nullable=True)

    participant_image_id = Column("PAR_IMAGE",UUID(as_uuid=True),ForeignKey(Image.id))

    participant_image = relationship("Image")

