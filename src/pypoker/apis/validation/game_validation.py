from datetime import datetime
from flask import jsonify
from pypoker import db
from pypoker.models.game import Game
from pypoker.apis.response.error_response import (
    Error, BadRequestResponse, InternalServerErrorResponse)
from pypoker.apis.response.valid_response import OKResponse


def validate_game(data):
    errors = []
    name = ""
    num_seats = 0
    turn_time = -1
    blind_levels = []
    blind_length = ""
    buyin = ""
    gtype = ""
    start_time = datetime.now()

    # Name
    if 'Name' not in data: 
        errors.append(Error(
            source="game.Name", 
            title="Missing required attribute", 
            detail="'Name' is required"
        ))
    else:
        name = data['Name']
    # NumSeats
    if 'NumSeats' not in data:
        errors.append(Error(
            source="game.NumSeats",
            title="Missing required attribute",
            detail="'NumSeats' is required"
        ))
    else:
        num_seats = data['NumSeats']
    # TurnTime
    turn_time = data['TurnTime'] if 'TurnTime' in data else -1
    # BlindLevels
    if 'BlindLevels' not in data:
        errors.append(Error(
            source="game.BlindLevels",
            title="Missing required attribute",
            detail="'BlindLevels' is required"
        ))
    else:
        blind_levels = data['BlindLevels']
        blind_levels = blind_levels.split(',')
        for level in blind_levels:
            l = level.split('_')
            if len(l) != 3 or l[0] != 'BLIND':
                errors.append(Error(
                    source="game.BlindLevels",
                    title="Invalid attribute",
                    detail="BlindLevel format: BLIND_SB_BB"
                ))
            if int(l[1]) >= int(l[2]):
                errors.append(Error(
                    source="game.BlindLevels",
                    title="Invalid attribute",
                    detail="BlindLevel - BB must be > SB"
                ))
        blind_levels = ','.join(blind_levels)
    # BlindLength
    if 'BlindLength' in data:
        blind_length = data['BlindLength']
        try:
            l = blind_length.split('_')
            if len(l) != 2 or (l[0] != 'MIN' and l[0] != 'TRN'):
                errors.append(Error(
                    source="game.BlindLength",
                    title="Invalid attribute",
                    detail="BlindLength format: MIN_N or TRN_N"
                ))
            int(l[1])
        except:
            errors.append(Error(
                source="game.BlindLength",
                title="Invalid attribute",
                detail=
"BlindLength format: MIN_N or TRN_N (N must be an int!)"
            ))
    # Buyin
    if 'Buyin' in data:
        buyin = data['Buyin']
        try:
            b = buyin.split('_')
            if len(b) != 3:
                errors.append(Error(
                    source="game.Buyin",
                    title="Invalid attribute",
                    detail="Buyin format: BUYIN_MIN_MAX"
                ))
            if b[0] != 'BUYIN':
                errors.append(Error(
                    source="game.Buyin",
                    title="Invalid attribute",
                    detail=
"Buyin format: BUYIN_MIN_MAX - missing 'BUYIN'"
                ))
            if int(b[1]) > int(b[2]):
                errors.append(Error(
                    source="game.Buyin",
                    title="Invalid attribute",
                    detail="Buyin: Max buyin can't be < Min buyin"
                ))
        except:
            errors.append(Error(
                source="game.Buyin",
                title="Invalid attribute",
                detail=
"Buyin format: BUYIN_MIN_MAX - 'MIN' and 'MAX' must be integers"
            ))
    # GameType
    if 'GameType' in data:
        gtype = data['GameType']
        if gtype != 'CASHGAME' and gtype != 'TOURNAMENT':
            errors.append(Error(
                source="game.GameType",
                title="Invalid attribute",
                detail=
"GameType format: accepts CASHGAME or TOURNAMENT"
            ))
    # StartTime
    if 'StartTime' in data:
        start_time = data['StartTime']
        if (start_time <= datetime.now()):
            BadRequestResponse("Start time must be in the future")
            errors.append(Error(
                source="game.GameType",
                title="Invalid attribute",
                detail="Start time must be in the future"
            ))
    if len(errors) != 0:
        return BadRequestResponse(errors)
    game = Game(name=name, num_seats=num_seats, turn_time=turn_time, 
                blind_levels=blind_levels, blind_length=blind_length,
                buyin=buyin, gtype=gtype, start_time=start_time)
    print('HERE2')
    if not game.create():
        return InternalServerErrorResponse([Error(
            title="Internal Server Error",
            detail="Unable to create game"
        )])
    return OKResponse(game.as_dict())