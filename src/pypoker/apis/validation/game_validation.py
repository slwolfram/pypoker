from datetime import datetime
from flask import jsonify
from pypoker import db
from pypoker.models.game import Game
from pypoker.apis.validation.response import bad_request, good_request

def validate_game_data(data):
    # Name
    if 'Name' not in data: 
        return bad_request("Request field 'Name' is required", 400)  
    name = data['Name']
    # NumSeats
    if 'NumSeats' not in data:
        return bad_request("Request field 'NumSeats' is required", 400)
    num_seats = data['NumSeats']
    # TurnTime
    turn_time = data['TurnTime'] if 'TurnTime' in data else -1
    # BlindLevels
    if 'BlindLevels' not in data:
        return bad_request(
            "Request field 'BlindLevels' is required", 400)
    blind_levels = data['BlindLevels']
    blind_levels = blind_levels.split(',')
    try:
        for level in blind_levels:
            l = level.split('_')
            if len(l) != 3 or l[0] != 'BLIND':
                return bad_request(
                    "BlindLevel format: BLIND_SB_BB", 400)
            if int(l[1]) >= int(l[2]):
                return bad_request(
                    "BlindLevel - BB must be > SB", 400)
    except:
        return bad_request("BlindLevel format: BLIND_SB_BB", 400)
    blind_levels = ','.join(blind_levels)
    # BlindLength
    blind_length = ""
    if 'BlindLength' in data:
        blind_length = data['BlindLength']
        try:
            l = blind_length.split('_')
            if len(l) != 2 or (l[0] != 'MIN' and l[0] != 'TRN'):
                return bad_request(
                    "BlindLength format: MIN_N or TRN_N", 400)
            int(l[1])
        except:
            return bad_request(
                "BlindLength format: MIN_N or TRN_N", 400)
    # Buyin
    buyin = ""
    if 'Buyin' in data:
        buyin = data['Buyin']
        try:
            b = buyin.split('_')
            if len(b) != 3:
                return bad_request('Buyin format: BUYIN_MIN_MAX', 400)
            if b[0] != 'BUYIN':
                return bad_request('Buyin format: BUYIN_MIN_MAX', 400)
            if b[1] > b[2]:
                return bad_request(
                    "Buyin: Max buyin can't be < Min buyin", 400)
        except:
            return bad_request('Buyin format: BUYIN_MIN_MAX', 400)
    # GameType
    gtype = ""
    if 'GameType' in data:
        gtype = data['GameType']
        if gtype != 'CASHGAME' and gtype != 'TOURNAMENT':
            return bad_request(
                "GameType format: accepts CASHGAME or TOURNAMENT", 400)
    # StartTime
    start_time = datetime.now()
    if 'StartTime' in data:
        start_time = data['StartTime']
        if (start_time <= datetime.now()):
            return bad_request("Start time must be in the future", 400)
    game = Game(name=name, num_seats=num_seats, turn_time=turn_time, 
                blind_levels=blind_levels, blind_length=blind_length, 
                buyin=buyin, gtype=gtype, start_time=start_time)
    db.create_all()
    db.session.add(game)
    db.session.commit()
    return good_request(game.as_dict(), 200)
