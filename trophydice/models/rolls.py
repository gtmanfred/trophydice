import uuid

from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from sqlalchemy.sql import expression

from trophydice.database import Base
from .rooms import Room


class Roll(Base):
    __tablename__ = "rolls"

    id = Column(BigInteger, primary_key=True)
    uid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    room_uid = Column(UUID(as_uuid=True), ForeignKey(Room.uid), nullable=False)
    dice = Column(JSONB, nullable=False)
    message = Column(String, nullable=False)
    max_die = Column(Integer, nullable=True)
    max_dark = Column(Integer, nullable=True)

    sequence = Sequence(f"{__tablename__}_seq", metadata=Base.metadata)
    seq_id = Column(BigInteger, sequence, server_default=sequence.next_value())
