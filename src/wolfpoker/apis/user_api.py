from flask import Flask, Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Api, Resource, fields, Namespace
from .api_decorators import token_required
from ..models.player import Player
from .validation.player_validation import validate_player
from ..models.user import User


api = Namespace('users', description='User related operations')



@api.route('/all')
class get_users(Resource):
    def get(self):
        users = User.query.all()
        if users is None:
            return bad_request('Unable to retrieve users', 500)
        users_dict = []
        for player in users:
            users_dict.append(user.as_dict())
        return good_request(users_dict, 200)


@api.route('/<int:id>')
class get_user(Resource):
    def get(self):
        user = User.fetch(id=id)
        if user is None:
            return bad_request('Unable to retrieve user', 400)
        return good_request(user.as_dict(), 200)


@api.route('/<int:id>/players')
class get_user_players(Resource):
    def get(self):
        pass

@api.route('/<int:id>/active-players')
class get_user_players(Resource):
    def get(self):
        pass