from datetime import datetime
from flask import jsonify
from pypoker import db
from pypoker.models.player import Player
from pypoker.apis.response.error_response import (
    Error, BadRequestResponse, InternalServerErrorResponse)
from pypoker.apis.response.valid_response import OKResponse


def validate_player(data):
    errors = []
    # Name
    if 'Name' not in data:
        errors.append(Error(
            source="player.Name",
            title="Missing Required Attribute",
            detail="Request field 'Name' is required"
        ))
    name = data['Name']

    player = Player(name=name, stack="", hand="", position="",
                    bet_amount="", is_active="", has_folded="",
                    is_winner="", has_moved="")
    if len(errors) != 0:
        return BadRequestResponse(errors)
    if not player.create():
        return InternalServerErrorResponse([Error(
            title="Internal Server Error",
            detail="Unable to create player"
        )])
    return OKResponse(player.as_dict())