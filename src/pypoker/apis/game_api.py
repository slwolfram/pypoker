from flask import Flask, Blueprint, jsonify
from flask_restplus import Api, Resource, fields, Namespace

from ..models.game import Game
from .validation.game_validation import validate_game
from .decorators import token_required


api = Namespace('games', description='Game related operations')
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


@api.route('/new')
class new_game(Resource):
    @api.expect(a_game)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        data = api.payload
        return validate_game(data)


@api.route('/all')
class get_games(Resource):
    def get(self):
        games = Game.query.all()
        if games is None:
            return {'error': 'Unable to retrieve games'}, 500, (
                   {'Access-Control-Allow-Origin': '*'})
        games_dict = []
        for game in games:
            games_dict.append(game.as_dict())
        return {'data': games_dict}, 200, (
               {'Access-Control-Allow-Origin': '*'})


@api.route('/<int:id>')
class get_game(Resource):
    def get(self, id):
        game = Game.fetch(id=id)
        if game is None:
            return {'error': 'Unable to retrieve game'}, 400, (
                   {'Access-Control-Allow-Origin': '*'})
        return {'data': game.as_dict()}, 200, (
               {'Access-Control-Allow-Origin': '*'})