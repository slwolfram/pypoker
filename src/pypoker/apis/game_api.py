from flask import Flask, Blueprint, jsonify
from flask_restplus import Api, Resource, fields, Namespace
from .api_decorators import token_required
from ..models.game import Game
from .validation.game_validation import validate_game


api = Namespace('games', description='Game related operations')


game_parser = api.parser()
game_parser.add_argument(
    'Name', 
    type=str, 
    required=True, 
    location='form', 
    help='The table name.')
game_parser.add_argument(
    'NumSeats', 
    type=int, 
    required=True, location='form', 
    help='Max number of players that can be seated.')
game_parser.add_argument(
    'TurnTime', 
    type=int, 
    location='form', 
    help="Max seconds a player can take to move. By default, players"
    " have infinite time.")
game_parser.add_argument(
    'Blinds', 
    type=str, 
    required=True, 
    location='form', 
    help="The blinds for each blind level." 
    " Format: 'SB1,BB1|SB2,BB2|..'")
game_parser.add_argument(
    'BlindLength', 
    type=str, 
    location='form', 
    help="The duration of each blind level. Can be in seconds or"
    " turns. Format: 'SEC_[N]' or 'TRN_[N]'. Uses first level if"
    " BlindLength is blank.")
game_parser.add_argument(
    'GameType', 
    type=str, 
    required=True, 
    location='form', 
    help="Specifies whether the game is a cash game or tournament,"
    " using 'CASHGAME' or 'TOURNAMENT'. Tournaments utilize blind"
    " levels and do not allow players to join once the game has"
    " started. The default value is 'CASHGAME'.")
game_parser.add_argument(
    'Buyin', 
    type=str, 
    required=True, 
    location='form', 
    help="The range of currency the player may start the game with."
    " Format: '[MIN]-[MAX]'")
game_parser.add_argument(
    'StartTime', 
    type=str, 
    location='form', 
    help="When the game will start. If not specified, cashgames start" 
    " when 2 or more players are active, and tournaments will start"
    " when the table is full.")

@api.route('/new')
class new_game(Resource):
    @api.doc(security='apikey', parser=game_parser)
    @token_required
    def post(self):
        data = game_parser.parse_args()
        r = validate_game(data)
        return r.get_response()


@api.route('/all')
class get_games(Resource):
    def get(self):
        games = Game.query.all()
        if games is None:
            return \
                {
                    'errors': {'error': 'Internal Server Error'},
                    'message': 'Internal Server Error'
                }, 500
        games_dict = []
        for game in games:
            games_dict.append(game.as_dict())
        return {'data': games_dict}, 200


@api.route('/<int:id>')
class get_game(Resource):
    def get(self, id):
        game = Game.fetch(id=id)
        if game is None:
            return \
                {
                    'errors': {'id': 'No matching game id in db'},
                    'message': 'Unable to fetch resource.'
                }, 400
        if game is -1:
            return \
                {
                    'errors': {'error': 'Internal Server Error'},
                    'message': 'Internal Server Error'
                }, 500
        return {'data': game.as_dict()}, 200