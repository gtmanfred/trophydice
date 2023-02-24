import uuid

from sqlalchemy import Boolean, Column, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from trophydice.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(BigInteger, primary_key=True)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    uid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
