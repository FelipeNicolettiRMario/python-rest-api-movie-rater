import uuid
from sqlalchemy import Column, ForeignKey, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base import Base
from models.image import Image

class User(Base):

    __tablename__ = "USU_USER"  


    id = Column("USU_ID",UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    name = Column("USU_NAME",String(40),nullable=False)
    password = Column("USU_PASSWORD",String(200),nullable=False)
    email = Column("USU_EMAIL",String(100),nullable=False,unique=True)
    description = Column("USU_DESCRIPTION",String(300))
    birthday = Column("USU_BIRTHDAY",Date,nullable=False)
    active_status = Column("USU_ACTIVE_STATUS",Boolean,default=True,nullable=False)
    profile_image_id = Column("USU_PROFILE_IMAGE",UUID(as_uuid=True),ForeignKey(Image.id))

    profile_image = relationship("Image")

    