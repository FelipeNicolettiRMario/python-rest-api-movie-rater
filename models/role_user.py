import uuid
from sqlalchemy import Column, ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import enum

from models.user import User

class E_ROLE(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    APPLICATION = "APPLICATION"

class RoleUser(Base):

    __tablename__ = "ROU_ROLE_USER"

    user_id = Column("ROU_USU_ID",UUID(as_uuid=True),ForeignKey(User.id),default=uuid.uuid4,nullable=False)
    role = Column("ROU_ROLE",Enum(E_ROLE),nullable=False,default=E_ROLE.USER)

    user = relationship("User",backref="User.roles")

    __table_args__ = (
        PrimaryKeyConstraint(user_id, role),
    )
