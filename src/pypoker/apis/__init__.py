from flask import Blueprint, request
from flask_restplus import Api
from .auth_api import api as auth_ns
from .game_api import api as game_ns
from .player_api import api as player_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint, 
          title='PyPoker', 
          version='1.0', 
          description='A fully featured Poker API', 
          authorizations={
            'apikey': 
            {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-API-Key'
            }
})

api.add_namespace(auth_ns)
api.add_namespace(game_ns)
api.add_namespace(player_ns)