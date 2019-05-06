from flask import Flask, Blueprint, jsonify
from flask_restplus import (
    Api, Resource, fields, Namespace, inputs)
from datetime import datetime
from .decorators.token_required import token_required
from .decorators.catch_api_exceptions import catch_api_exceptions
from ..models.game import Game
from ..models.game_state import GameState
from ..models.table_state import TableState


api = Namespace('games', description='Game related operations')


game_parser = api.parser()
game_parser.add_argument(
    'Name', 
    type=inputs.regex('^[a-zA-Z][a-zA-Z0-9@\.]{1,16}$'),
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
    type=inputs.regex('^[0-9]+,[0-9]+(\|[0-9]+,[0-9]+)*$'), 
    required=True, 
    location='form', 
    help="The blinds for each blind level." 
    " Format: 'SB1,BB1|SB2,BB2|..'")
game_parser.add_argument(
    'BlindLength', 
    type=inputs.regex('^(SEC|TRN)_[0-9]+$'), 
    location='form', 
    help="The duration of each blind level. Can be in seconds or"
    " turns. Format: 'SEC_[N]' or 'TRN_[N]'. Uses first level if"
    " BlindLength is blank.")
game_parser.add_argument(
    'GameFormat', 
    type=inputs.regex('^(CASHGAME|TOURNAMENT)$'), 
    location='form', 
    help="Specifies whether the game is a cash game or tournament,"
    " using 'CASHGAME' or 'TOURNAMENT'. Tournaments utilize blind"
    " levels and do not allow players to join once the game has"
    " started. The default value is 'CASHGAME'.")
game_parser.add_argument(
    'GameType', 
    type=inputs.regex('^(TexasHoldem)$'),
    location='form', 
    help="The Poker variation. Currently, only 'TexasHoldem' is" 
    " supported.")
game_parser.add_argument(
    'Buyin', 
    type=inputs.regex('^[1-9][0-9]*,[1-9][0-9]*$'), 
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
    @catch_api_exceptions
    @token_required
    def post(self, **kwargs):
        data = game_parser.parse_args()
        name = data['Name']
        num_seats = data['NumSeats']
        turn_time = data['TurnTime'] if data['TurnTime'] else -1
        blinds = data['Blinds']
        blind_length = data['BlindLength'] \
            if data['BlindLength'] else ""
        game_type = data['GameType'] \
            if data['GameType'] else 'TexasHoldem'
        game_format = data['GameFormat'] \
            if data['GameFormat'] else 'CASHGAME'
        buyin = data['Buyin']
        buyin_v = buyin.split(',')
        if (int(buyin_v[0]) > int(buyin_v[1])): return (
                {
                    'errors': {'Buyin': 'Invalid value.'},
                    'message': 'Min Buyin must be LTE to Max Buyin'
                }, 400)
        start_time =  datetime.now()
        if (data['StartTime']):
            try:
                start_time = datetime.strptime(
                    data['StartTime'], '%Y-%m-%d %H:%M:%S')
            except: return (
                {
                    'errors': {'StartTime': 'Invalid value.'},
                    'message': '{} is not a valid date/time'.format(
                        data['StartTime'])
                }, 400)
            if (start_time < datetime.now()): return (
                {
                    'errors': {'StartTime': 'Invalid value.'},
                    'message': 'StartTime must be in the future'
                }, 400)
        game = Game(name, num_seats, turn_time, blinds, blind_length, 
                    buyin, game_type, game_format, start_time).create()
        return {"data": game.as_dict()}, 200


@api.route('/<string:guid>')
class game(Resource):
    @api.doc(security='apikey')
    @catch_api_exceptions
    @token_required
    def delete(self, guid, **kwargs):
        game = Game.fetch(guid=guid)
        if game.delete() == True:
            return {'message': 'Successfully deleted game.'}, 200
        else:
            return {'error': "Couldn't delete game"}, 400


    @catch_api_exceptions
    def get(self, guid):
        game = Game.fetch(guid=guid)
        if game is None: return (
            {
                'errors': {'id': 'No matching game id in db'},
                'message': 'Unable to fetch resource.'
            }, 400)
        return {'data': game.as_dict()}, 200


@api.route('/all')
class get_games(Resource):
    @catch_api_exceptions
    def get(self):
        games = Game.query.all()
        games_dict = [g.as_dict for g in games]
        return {'data': games_dict}, 200


game_parser = api.parser()
game_parser.add_argument(
    'SeatID', 
    type=int,
    location='form', 
    help='The seat id.')
game_parser.add_argument(
    'Stack', 
    type=float,
    location='form', 
    help="The player's stack.")
@api.route('/<string:game_guid>/join')
class join_game(Resource):
    @api.doc(security='apikey')
    @catch_api_exceptions
    @token_required
    def post(self, game_guid, seat_id, **kwargs):
        pass
