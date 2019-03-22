from datetime import datetime
from flask import jsonify
from pypoker import db
from pypoker.models.player import Player
from pypoker.apis.validation.response import bad_request, good_request

def validate_game_data(data):
    # Name
    if 'Name' not in data: 
        return bad_request("Request field 'Name' is required", 400)  
    name = data['Name']

    player = Player(name=name, stack="", hand="", position="",
                    bet_amount="", is_active="", has_folded="",
                    is_winner="", has_moved="")
    db.create_all()
    db.session.add(game)
    db.session.commit()
    return good_request(game.as_dict(), 200)
