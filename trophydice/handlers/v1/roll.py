import json
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID
from uuid import uuid4

import dicetray
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import Header
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from trophydice.socketio import sm

router = APIRouter()


class DiceTypeEnum(str, Enum):
    dark = 'dark'
    light = 'light'
    gold = 'gold'


class Dice(BaseModel):
    highest: bool
    result: int
    dice_type: DiceTypeEnum
    link: Optional[str]

    @validator('link', always=True)
    def make_image_name(cls, v, values, **kwargs):
        result = values['result']
        dtype = values['dice_type']
        if dtype is DiceTypeEnum.gold:
            result = result // 6
        return f'/dice/d6-{dtype.value}-{result}.png'


class Roll(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    dice: List[Dice]
    max_die: Optional[int]
    max_dark: Optional[int]


class Response(Roll):
    message: str


async def emit(roll, resp, room=None):
    if room is not None:
        await sm.emit(f'v1/{roll}', json.loads(resp.json()), room)


async def headers(x_room: Optional[str] = Header(None), x_user_name: Optional[str] = Header(None)):
    return {
        'room': x_room,
        'user': f'<strong>{x_user_name}</strong>',
    }


def roll(light, dark):
    tray = dicetray.Dicetray(f'{light + dark}d6')
    tray.roll()
    max_die = max(tray.dice)
    response = []
    for _ in range(light):
        dice = tray.dice.pop()
        response.append(Dice(
            highest=dice.result == max_die.result,
            result=dice.result,
            dice_type=DiceTypeEnum.light,
        ))
    if tray.dice:
        max_dark = max(tray.dice)
        for dice in tray.dice:
            response.append(Dice(
                highest=dice.result == max_die.result,
                result=dice.result,
                dice_type=DiceTypeEnum.dark,
            ))
        return Roll(
            dice=response,
            max_die=max_die.result,
            max_dark=max_dark.result,
        )
    return Roll(
        dice=response,
        max_die=max_die.result,
        max_dark=0,
    )


@router.get('/risk', response_model=Response, tags=["rolls"], operation_id="risk")
async def do_risk_roll(light: int, dark: Optional[int] = 0, headers: Dict = Depends(headers)):
    result = roll(light, dark)
    message = f'<p>{headers["user"]} rolled a {result.max_die}'
    if result.max_dark == result.max_die:
        message += ' (dark). If this is higher than your Ruin, your Ruin goes up by 1'
    elif result.max_die < 6:
        message += '. You can add a dark die and re-roll'
    message += '.</p>'

    resp = Response(
        message=message,
        dice=result.dice,
        max_die=result.max_die,
        max_dark=result.max_dark or None,
    )
    await emit('risk', resp, headers['room'])
    return resp


@router.get('/gold', response_model=Response, tags=["rolls"], operation_id="gold")
async def do_gold_roll(gold: int, headers: Dict = Depends(headers)):
    tray = dicetray.Dicetray(f'{gold}d6')
    tray.roll()
    count = len([die for die in tray.dice if die.result == 6])
    response = []
    for die in tray.dice:
        response.append(Dice(
            highest=die.result == 6,
            result=die.result,
            dice_type=DiceTypeEnum.gold,
        ))
    resp = Response(
        message=f'Found got {count} Gold.',
        dice=response,
    )
    await emit('gold', resp, headers['room'])
    return resp


@router.get('/ruin', response_model=Response, tags=["rolls"], operation_id="ruin")
async def do_ruin_roll(headers: Dict = Depends(headers)):
    result = roll(light=0, dark=1)
    message = f'{headers["user"]}\'s Ruin goes up if it\'s currently less than {result.max_die}.'
    resp = Response(
        message=message,
        max_die=result.max_die,
        dice=result.dice,
    )
    await emit('ruin', resp, headers['room'])
    return resp


@router.get('/combat', response_model=Response, tags=["rolls"], operation_id="combat")
async def do_combat_roll(dark: int, headers: Dict = Depends(headers)):
    result = roll(light=0, dark=dark)
    order = sorted(result.dice, key=lambda x: x.result, reverse=True)
    if len(order) == 1:
        final = order[0].result
    else:
        final = order[0].result + order[1].result
        order[1].highest = True
    for die in order[2:]:
        die.highest = False
    message = f'The monster is defeated if its Endurance is {final} or less.'
    resp = Response(
        message=message,
        dice=result.dice,
    )
    await emit('combat', resp, headers['room'])
    return resp


@router.get('/weak', response_model=Response, tags=["rolls"], operation_id="weak")
async def do_weak_roll(headers: Dict = Depends(headers)):
    result = roll(light=1, dark=0)
    message = f'{headers["user"]}\'s Weak Point is {result.max_die}.'
    resp = Response(
        message=message,
        max_die=result.max_die,
        dice=result.dice,
    )
    await emit('weak', resp, headers['room'])
    return resp


@router.get('/help', response_model=Response, tags=["rolls"], operation_id="help")
async def do_help_roll(headers: Dict = Depends(headers)):
    result = roll(light=1, dark=0)
    resp = Response(
        message=f'{headers["user"]} rolled a {result.max_die}. If this matches any dark die, their ruin goes up by 1.',
        dice=result.dice,
        max_die=result.max_die,
    )
    await emit('help', resp, headers['room'])
    return resp


@router.get('/hunt', response_model=Response, tags=["rolls"], operation_id="hunt")
async def do_hunt_roll(light: int, headers: Dict = Depends(headers)):
    result = roll(light=light, dark=0)
    if result.max_die >= 4:
        message = f'{headers["user"]} gets a token'
        if result.max_die < 6:
            message += ', but encounters something terrible'
    else:
        message = f'{headers["user"]} encounters something terrible'
        if result.max_die == 1:
            message += ', and loses all tokens'
    message += '.'
    resp = Response(
        message=message,
        dice=result.dice,
        max_die=result.max_die,
    )
    await emit('hunt', resp, headers['room'])
    return resp
      

@router.get('/contest', response_model=Response, tags=["rolls"], operation_id="contest")
async def do_contest_roll(
    light: int,
    dark: int,
    tasks: BackgroundTasks,
    users: Union[str, None] = None,
    headers: Dict = Depends(headers),
):
    result = roll(light, dark)
    message = f'{headers["user"]} was in a contest. '
    ruin = len([die for die in result.dice if die.result == 1 and die.dice_type is DiceTypeEnum.dark])
    if ruin:
        message += f'Their ruin went up by {ruin}. '
    die_count = {6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for die in result.dice:
        die_count[die.result] += 1
    message += str(die_count)

    resp = Response(
        message=message,
        dice=result.dice,
    )
    await emit('contest', resp, headers['room'])
    return resp


@router.get('/reduction', response_model=Response, tags=["rolls"], operation_id="reduction")
async def do_reduction_roll(headers: Dict = Depends(headers)):
    result = roll(light=1, dark=0)
    resp = Response(
        message=(
            f'{headers["user"]} rolled a {result.max_die}. If this is less than your current Ruin, '
            'your betrayal goes unnoticed and you decrease your Ruin by 1'
        ),
        dice=result.dice,
        max_die=result.max_die,
    )
    await emit('reduction', resp, headers['room'])
    return resp
