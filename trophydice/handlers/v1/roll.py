from enum import Enum
from typing import List
from typing import Optional

import dicetray
from fastapi import APIRouter
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

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
        return f'/dice/d6-{dtype}-{result}.png'


class Roll(BaseModel):
    dice: List[Dice]
    max_die: Optional[int]
    max_dark: Optional[int]


class Response(Roll):
    message: str



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


@router.get('/risk', response_model=Response)
def do_risk_roll(light: int, dark: Optional[int] = 0):
    result = roll(light, dark)
    message = f'Rolled a {result.max_die}'
    if result.max_dark == result.max_die:
        message += ' (dark) . If this is higher than your Ruin, your Ruin goes up by 1'
    elif result.max_die < 6:
        message += '. You can add a dark die and re-roll'
    message += '.'

    return Response(
        message=message,
        dice=result.dice,
        max_die=result.max_die,
        max_dark=result.max_dark or None,
    )


@router.get('/gold', response_model=Response)
def do_gold_roll(gold: int):
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
    return Response(
        message=f'got {count} Gold.',
        dice=response,
    )


@router.get('/ruin', response_model=Response)
def do_ruin_roll():
    result = roll(light=0, dark=1)
    message = f'Ruin goes up if it\'s currently less than {result.max_die}.'
    return Response(
        message=message,
        max_die=result.max_die,
        dice=result.dice,
    )


@router.get('/combat', response_model=Response)
def do_combat_roll(dark: int):
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
    return Response(
        message=message,
        dice=result.dice,
    )


@router.get('/weak', response_model=Response)
def do_weak_roll():
    result = roll(light=1, dark=0)
    message = f'Weak Point is {result.max_die}.'
    return Response(
        message=message,
        max_die=result.max_die,
        dice=result.dice,
    )


@router.get('/help', response_model=Response)
def do_help_roll():
    result = roll(light=1, dark=0)
    return Response(
        message=f'rolled a {result.max_die}. If this matches any dark die, their ruin goes up by 1.',
        dice=result.dice,
        max_die=result.max_die,
    )


@router.get('/hunt', response_model=Response)
def do_hunt_roll(light: int):
    result = roll(light=light, dark=0)
    if result.max_die >= 4:
        message = 'gets a token'
        if result.max_die < 6:
            message += ', but encounters something terrible'
    else:
        message = 'encounters something terrible'
        if result.max_die == 1:
            message += ', and loses all tokens'
    message += '.'
    return Response(
        message=message,
        dice=result.dice,
        max_die=result.max_die,
    )
      

@router.get('/contest', response_model=Response)
def do_contest_roll(light: int, dark: int):
    result = roll(light, dark)
    message = 'was in a contest.'
    ruin = len([die for die in result.dice if die.result == 1])
    if ruin:
        message += f' Their ruin went up by {ruin}.'

    return Response(
        message=message,
        dice=result.dice,
    )


@router.get('/reduction', response_model=Response)
def do_reduction_roll():
    result = roll(light=1, dark=0)
    return Response(
        message=(
            f'rolled a {result.max_die}. If this less than your current Ruin, '
            'your betrayal goes unnoticed and you decrease your Ruin by 1'
        ),
        dice=result.dice,
        max_die=result.max_die,
    )
