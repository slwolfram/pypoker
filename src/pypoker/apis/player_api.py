from flask import Flask, Blueprint, jsonify
from flask_restplus import Api, Resource, fields

player = Blueprint('player', __name__)
api = Api(player)

from pypoker.models.game import Game
from pypoker.apis.validation.game_validation import validate_game_data
from pypoker.apis.validation.response import bad_request, good_request

a_player = api.model(
    'a_player', {
        'Name': fields.String(
            required=True, 
            description= "The player's name"
        ),
        'Position': fields.Integer(
            required=True,
            description=(
"An integer representation of the player's position"
        )),
        'Stack': fields.Integer(
            description=(
"An integer representation of the player's stack (currency, chip \
value, etc.)"
        ))
    }
)

def fold(self, game):
    if (self.bet_amount == game.highest_bet):
        print("You can't fold if you can check.")
        return False
    print("{} folds.".format(self.name))
    self.has_folded = True
    return True

def bet(self, amount, game):
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

def check_call(self, game):
    if (self.bet_amount == game.highest_bet):
        print("{} checks".format(self.name))
        return True
    else:
        call_value = game.highest_bet - self.bet_amount
        self.bet(call_value, game)
        return True
