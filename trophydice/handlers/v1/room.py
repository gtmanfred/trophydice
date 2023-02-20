from typing import Optional
from uuid import UUID
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from trophydice.database import get_db
from trophydice.models.rooms import Room
from trophydice.models.rolls import Roll as RollModel

from .roll import Response as BaseRoll

router = APIRouter()


class Response(BaseModel):
    uid: UUID

    class Config:
        orm_mode = True


class Roll(BaseRoll):
    class Config:
        orm_mode = True


class Rolls(BaseModel):
    results: list[Roll]
    more_data: bool
    seq_id: int


@router.post(
    "/room", response_model=Response, tags=["room"], operation_id="create_room"
)
async def create_room(db: Session = Depends(get_db)):
    room = Room()
    db.add(room)
    db.commit()
    return room


@router.get(
    "/room/{room_uid}", response_model=Rolls, tags=["room"], operation_id="get_room"
)
async def get_room(
    room_uid: UUID, seq_id: Optional[int] = 0, db: Session = Depends(get_db)
):
    rolls = db.query(RollModel).filter(
        RollModel.room_uid == room_uid,
        RollModel.seq_id > seq_id,
    ).limit(100).all()

    if rolls:
        more_data = bool(
            db.query(RollModel).filter(
                RollModel.room_uid == room_uid,
                RollModel.seq_id > rolls[-1].seq_id,
            ).count()
        )
        seq_id = rolls[-1].seq_id
    else:
        more_data = False
        seq_id = seq_id

    return {
        "results": rolls,
        "more_data": more_data,
        "seq_id": seq_id,
    }
