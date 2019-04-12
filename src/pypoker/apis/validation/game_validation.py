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
    blinds = ""
    blind_level = 0
    blind_length = ""
    buyin = ""
    gtype = "CASHGAME"
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
    # Blinds
    if 'Blinds' not in data:
        errors.append(Error(
            source="game.Blinds",
            title="Missing required attribute",
            detail="'Blinds' is required"
        ))
    else:
        blinds = data['Blinds']
        blinds = blinds.split('|')
        try:
            for level in blinds:
                l = level.split(',')
                if len(l) != 2:
                    errors.append(Error(
                        source="game.Blinds",
                        title="Invalid attribute",
                        detail="Format: 'SB,BB'"
                    ))
                elif int(l[0]) >= int(l[1]):
                    errors.append(Error(
                        source="game.Blinds",
                        title="Invalid attribute",
                        detail="Blinds - BB must be > SB"
                    ))
            blinds = '|'.join(blinds)
        except:
            errors.append(Error(
                source="game.Blinds",
                title="Invalid attribute",
                detail="Blind format: 'SB,BB'"
            ))
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
                detail="BlindLength format: MIN_N or TRN_N"
                       "(N must be an int!)"
            ))
    # Buyin
    
    if 'Buyin' not in data:
        errors.append(Error(
            source="game.Buyin",
            title="Missing required attribute",
            detail="'Buyin' is required"
        ))
    else:
        buyin = data['Buyin']
        if buyin != "":
            try:
                b = buyin.split('-')
                if len(b) != 2:
                    errors.append(Error(
                        source="game.Buyin",
                        title="Invalid attribute",
                        detail="Buyin format: BUYIN_MIN_MAX"
                    ))
                if int(b[0]) > int(b[1]):
                    errors.append(Error(
                        source="game.Buyin",
                        title="Invalid attribute",
                        detail="Buyin: Max buyin can't be < Min buyin"
                    ))
                if int(b[0]) <= 0 or int(b[1]) <= 0:
                    errors.append(Error(
                        source="game.Buyin",
                        title="Invalid attribute",
                        detail="Buyin: Values must be > 0"
                    ))
            except:
                errors.append(Error(
                    source="game.Buyin",
                    title="Invalid attribute",
                    detail="Buyin format: BUYIN_MIN_MAX - 'MIN' and"
                        " 'MAX' must be integers"
                ))
    # GameType
    if 'GameType' in data:
        gtype = data['GameType']
        if gtype == "": gtype = 'CASHGAME'
        if gtype != 'CASHGAME' and gtype != 'TOURNAMENT':
            errors.append(Error(
                source="game.GameType",
                title="Invalid attribute",
                detail="GameType format: accepts CASHGAME or"
                       " TOURNAMENT"
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
                blinds=blinds, blind_level=blind_level,
                blind_length=blind_length, buyin=buyin,
                gtype=gtype, start_time=start_time)
    print('HERE2')
    if not game.create():
        return InternalServerErrorResponse([Error(
            title="Internal Server Error",
            detail="Unable to create game"
        )])
    return OKResponse(game.as_dict())