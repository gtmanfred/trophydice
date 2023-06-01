import json
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

import dicetray
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from trophydice.socketio import sm

router = APIRouter()

class DiceColorEnum(str, Enum):
    dark = 'dark'
    light = 'light'
    red = 'red'
    blue = 'blue'
    green = 'green'
    yellow = 'yellow'


class Dice(BaseModel):
    highest: bool
    result: int
    dice_type: DiceColorEnum
    link: Optional[str]

    @validator('link', always=True)
    def make_image_name(cls, v, values, **kwargs):
        result = values['result']
        dtype = values['dice_type'].value
        return f'/dice/d6-{dtype}-{result}.png'


class Roll(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    dice: List[Dice]
    max_die: int


class Response(Roll):
    message: str


async def emit(roll, resp, room=None):
    if room is not None:
        await sm.emit(f'v2/{roll}', json.loads(resp.json()), room)


async def headers(x_room: Optional[str] = Header(None), x_user_name: Optional[str] = Header(None)):
    return {
        'room': x_room,
        'user': f'<strong>{x_user_name}</strong>',
    }


def _do_roll(rolls: Dict[DiceColorEnum, int]):
    tray = dicetray.Dicetray(f'{sum(rolls.values())}d6')
    tray.roll()
    if not tray.dice:
        raise HTTPException(status_code=400, detail="no dice specified")
    max_die = max(tray.dice)
    response = []
    for dice_type, count in rolls.items():
        for _ in range(count):
            die = tray.dice.pop()
            response.append(Dice(
                highest = die.result == max_die.result,
                result = die.result,
                dice_type=dice_type,
            ))
    return Roll(dice=response, max_die=max_die.result)


@router.post('/roll', response_model=Response, tags=["rolls"], operation_id="roll")
async def do_roll(rolls: Dict[DiceColorEnum, int] = None, headers: Dict = Depends(headers)):
    result = _do_roll(rolls)
    resp = Response(
        message=f'{headers["user"]} rolled a {result.max_die}.',
        dice=result.dice,
        max_die=result.max_die,
    )
    await emit('roll', resp, headers['room'])
    return resp
