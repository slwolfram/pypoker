import os
from datetime import datetime
from flask import Flask, Blueprint, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

create_game = Blueprint('create_game', __name__)
api = Api(create_game)

from pypoker.models.game import Game
from pypoker import db
new_game = api.model(
    'new_game', {
        'name': fields.String(
            required=True, 
            description='The table name of the game to be created.'
        ),
        'num_seats': fields.Integer(
            required=True,
            description='Max number of players that can be seated.'
        ),
        'turn_time': fields.Integer(
            description='The max seconds a player can take to make a move. \
                By default, gives players infinite time to make a move.'
        ),
        'blind_levels': fields.String(
            required=True,
            description='An comma-separated list of blinds, with the \
                format BLIND_SB_BB.'
        ),
        'blind_length': fields.String(
            description='The duration of each blind level. Can be either \
                in minutes or turns, with the format MIN_N or TRN_N. \
                By default, only uses first blind_level'
        ),
        'buyin': fields.String(
            description='Specifies buyin, with the format BUYIN_MIN_MAX. \
                By default, no max or min buyin is specified'
        ),
        'type': fields.String(
            description='Specifies whether the game is a cash game or \
                tournament, with the format CASHGAME or TOURNAMENT. Tournaments \
                enable blind levels and do not allow new players to join \
                once the game has started. The default value is CASHGAME.'
        ),
        'start_time': fields.DateTime(
            description='Specifies when the game will start. Required for \
                tournaments. For cash games, if not specified, the game \
                will start when 2 or more players have joined.'
        )

})

@api.route('/create')
class games(Resource):
    @api.expect(new_game)
    def post(self):
        data = api.payload
        name = data['name']
        num_seats = data['num_seats']
        if 'turn_time' in data:
            turn_time = data['turn_time']
        else:
            turn_time = -1
        blind_levels = data['blind_levels']
        # data validation for blind levels
        blind_levels = blind_levels.split(',')
        try:
            for level in blind_levels:
                l = level.split('_')
                if len(l) != 3:
                    pass
                if l[0] != 'BLIND':
                    pass
                if int(l[1]) >= int(l[2]):
                    pass
        except:
            pass
        blind_levels = ','.join(blind_levels)
        if 'blind_length' in data:
            blind_length = data['blind_length']
            try:
                l = blind_length.split('_')
                if len(l) != 2:
                    pass
                if l[0] != 'MIN' and l[0] != 'TRN':
                    pass
                int(l[1])
            except:
                pass
        else:
            blind_length = ""
        # data validation for blind length
        if 'buyin' in data:
            buyin = data['buyin']
            try:
                b = buyin.split('_')
                if len(b) != 3:
                    pass
                if b[0] != 'BUYIN':
                    pass
                if b[1] > b[2]:
                    pass
            except:
                pass
        else:
            buyin = ""
        if 'type' in data:
            gtype = data['type']
            if gtype != 'CASHGAME' and gtype != 'TOURNAMENT':
                pass
        else:
            gtype = ""
        if 'start_time' in data:
            start_time = data['start_time']
            if (start_time <= datetime.now()):
                pass
        else:
            start_time = datetime.now()
        game = Game(name=name, 
                    num_seats=num_seats, 
                    turn_time=turn_time, 
                    blind_levels=blind_levels, 
                    blind_length=blind_length, 
                    buyin=buyin, 
                    gtype=gtype, 
                    start_time=start_time)
        db.create_all()
        db.session.add(game)
        db.session.commit()
        print(game.as_dict())
        data = game.as_dict()
        response = jsonify(data)
        response.status_code = 200
        return response