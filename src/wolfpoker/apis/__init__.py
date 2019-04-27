from flask import Blueprint, request
from flask_restplus import Api
from .auth_api import api as auth_ns
from .game_api import api as game_ns
from .player_action_api import api as player_action_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint, 
          title='WolfPoker', 
          version='1.0', 
          description='A fully featured Poker API', 
          authorizations={
            'apikey': 
            {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
})

api.add_namespace(auth_ns)
api.add_namespace(game_ns)
api.add_namespace(player_action_ns)