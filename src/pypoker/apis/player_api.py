from flask import Flask, Blueprint, jsonify
from flask_restplus import Api, Resource, fields

player = Blueprint('player', __name__)
api = Api(player)

from pypoker.models.player import Player
from pypoker.apis.validation.player_validation import validate_player_data
from pypoker.apis.validation.response import bad_request, good_request

a_player = api.model(
    'a_player', {
        'Name': fields.String(
            description= "The player's name"
        ),
        'Stack': fields.Integer(
            required=True,
            description=(
"An integer representation of the player's stack (currency, chip \
value, etc.)"
        ))
    }
)

a_bet = api.model(
    'a_bet', {
        'BetAmount': fields.Integer(
            required=True,
            description="The amount of currency being wagered"
        )
    }
)

@api.route('/games/<int:id>/join')
class join_game(Resource):
    @api.expect(a_player)
    def post(self, id):
        data = api.payload
        pass

@api.route('/games/<int:game_id>/join/<int:seat_id>')
class join_game(Resource):
    @api.expect(a_player)
    def post(self, game_id, seat_id):
        data = api.payload
        pass

@api.route('/games/<int:game_id>/leave')
class join_game(Resource):
    def post(self):
        pass

@api.route('/players/<int:id>/fold')
class fold(Resource):
    def fold(self, id):
        """
        if (self.bet_amount == game.highest_bet):
            print("You can't fold if you can check.")
            return False
        print("{} folds.".format(self.name))
        self.has_folded = True
        return True
        """
        pass

@api.route('/players/<int:id>/bet')
class bet(Resource):
    @api.expect(a_bet)
    def bet(self, id):
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

@api.route('/players/<int:id>/call')
@api.route('/players/<int:id>/check')
class checkcall(Resource):
    def post(self, id):
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
