from flask import Flask, Blueprint, jsonify
from flask_restplus import Api, Resource, fields

games = Blueprint('games', __name__)
api = Api(games)

from pypoker.models.game import Game
from pypoker.apis.validation.game_validation import validate_game_data
from pypoker.apis.validation.response import bad_request, good_request

a_game = api.model(
    'a_game', {
        'Name': fields.String(
            required=True, 
            description= 'The table name of the game to be created.'
        ),
        'NumSeats': fields.Integer(
            required=True,
            description= 'Max number of players that can be seated.'
        ),
        'TurnTime': fields.Integer(
            description=(
'The max seconds a player can take to make a move. By default, gives \
players infinite time to make a move.'
        )),
        'BlindLevels': fields.String(
            required=True,
            description=(
'An comma-separated list of blinds, with the format BLIND_SB_BB.'
        )),
        'BlindLength': fields.String(
            description=(
'The duration of each blind level. Can be either in minutes or turns. \
Format: MIN_N or TRN_N. Uses first BlindLevel if BlindLength not given'
        )),
        'Buyin': fields.String(
            description=(
'Specifies buyin, with the format BUYIN_MIN_MAX. By default, no max \
or min buyin is specified'
        )),
        'GameType': fields.String(
            description=(
'Specifies whether the game is a cash game or tournament, with the \
format CASHGAME or TOURNAMENT. Tournaments enable blind levels and \
do not allow new players to join once the game has started. The \
default value is CASHGAME.'
        )),
        'StartTime': fields.DateTime(
            description=(
'Specifies when the game will start. Required for tournaments. For \
cash games, if not specified, the game will start when 2 or more \
players have joined.'
        ))
    }
)

@api.route('/games')
class games_api(Resource):
    @api.expect(a_game)
    def post(self):
        data = api.payload
        return validate_game_data(data)

    def get(self):
        games = Game.query.all()
        games_dict = []
        for game in games:
            print(game)
            games_dict.append(game.as_dict())
        return good_request(games_dict, 200)

@api.route('/games/<int:id>')
@api.param('id', 'The game identifier')
class game_api(Resource):
    @api.doc('get_game')
    def get(self, id):
        try:
            game = Game.query.filter_by(id=int(id)).first()
        except:
            return bad_request('Game not found', 404)
        return good_request(game.as_dict(), 200)