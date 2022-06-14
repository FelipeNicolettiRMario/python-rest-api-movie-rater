import uuid
from models.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Enum
import enum

class E_MEDIA_STORAGE_TYPE(enum.Enum):
    S3 = 'S3'
    FILE_SERVER = 'FILE_SERVER'
    LOCAL = 'LOCAL'

class E_IMAGE_TYPE(enum.Enum):
    PROFILE = 'PROFILE'
    MOVIE = 'MOVIE'
    PARTICIPANT = 'PARTICIPANT'

class Image(Base):

    __tablename__ = "IMG_IMAGE"

    id = Column("IMG_ID",UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    path = Column("IMG_PATH",String(300),nullable=False)
    storage_type = Column("IMG_STORAGE_TYPE",Enum(E_MEDIA_STORAGE_TYPE),nullable=False,default=E_MEDIA_STORAGE_TYPE.LOCAL)
    image_type = Column("IMG_IMAGE_TYPE",Enum(E_IMAGE_TYPE),nullable=False)