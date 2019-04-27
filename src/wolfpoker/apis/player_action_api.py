from flask import Flask, Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Api, Resource, fields, Namespace
from ..models.player import Player
from ..models.player_state import PlayerState
from ..models.player_action import PlayerAction
from .api_decorators import token_required
from ..models.user import User


api = Namespace('player-actions', description='Player related operations')


@api.route('/all')
class get_players(Resource):
    def get(self):
        players = Player.fetch_all()
        if players == -1:
            r = InternalServerErrorResponse(
                [Error("Backend Error")])
            return r.get_response()
        if players == None:
            players = []
        players_dict = []
        for player in players:
            players_dict.append(player.as_dict())
        r = OKResponse(players_dict)
        return r.get_response()


@api.route('/<int:id>')
class get_player(Resource):
    def get(self):
        player = Player.fetch(id=id)
        if player is None:
            r = BadRequestResponse(
                [Error("Player Doesn't Exist")])
            return r.get_response()
        if player == -1:
            r = InternalServerErrorResponse(
                [Error("Backend Error")])
            return r.get_response()
        
        return good_request(player.as_dict(), 200)


@api.route('/join')
class join_game(Resource):
    @api.doc(security='apikey')
    @token_required
    def post(self, id):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        data = api.payload
        pass


@api.route('/leave')
class leave_game(Resource):
    @api.doc(security='apikey')
    @token_required
    def post(self):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        pass


@api.route('/sitout')
class sitout(Resource):
    @api.doc(security='apikey')
    @token_required
    def post(self, id):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        """
        if (self.bet_amount == game.highest_bet):
            print("{} checks".format(self.name))
            return True
        else:
            call_value = game.highest_bet - self.bet_amount
            self.bet(call_value, game)
            return True
        """
        pass


@api.route('/fold')
class fold(Resource):
    @api.doc(security='apikey')
    @token_required
    def fold(self, id):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        """
        if (self.bet_amount == game.highest_bet):
            print("You can't fold if you can check.")
            return False
        print("{} folds.".format(self.name))
        self.has_folded = True
        return True
        """
        pass


@api.route('/bet')
class bet(Resource):
    @api.doc(security='apikey')
    @token_required
    def bet(self, id):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        data = api.payload
        """
        if (amount + self.bet_amount >= game.highest_bet):
            if (amount + self.bet_amount == game.highest_bet):
                print("{} calls for ${}".format(self.name, amount))
            else:
                print("{} bets ${}".format(self.name, amount))
            self.cash -= amount
            self.bet_amount += amount
            game.highest_bet = self.bet_amount
            game.pot += amount
            return True
        else:
            print("Invalid bet amount: {}".format(amount))
            return False
        """
        pass


@api.route('/call')
class call(Resource):
    @api.doc(security='apikey')
    @token_required
    def post(self, id):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        """
        if (self.bet_amount == game.highest_bet):
            print("{} checks".format(self.name))
            return True
        else:
            call_value = game.highest_bet - self.bet_amount
            self.bet(call_value, game)
            return True
        """
        pass


@api.route('/check')
class check(Resource):
    @api.doc(security='apikey')
    @token_required
    def post(self, id):
        user = User.verify_auth_token(request.headers['X-API-KEY'])
        print(user.as_dict())
        """
        if (self.bet_amount == game.highest_bet):
            print("{} checks".format(self.name))
            return True
        else:
            call_value = game.highest_bet - self.bet_amount
            self.bet(call_value, game)
            return True
        """
        pass