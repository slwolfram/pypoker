from datetime import datetime
from pypoker import db
from pypoker.models.table_state import TableState


class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship(
        'Game', back_populates='game_state_current')
    # -1 - Waiting to start
    #  0 - Round reset
    #  1 - Preflop
    #  2 - Flop
    #  3 - Turn
    #  4 - River
    #  5 - Evaluating hands
    #  6 - Distribute winnings
    game_state = db.Column(db.String, nullable=False)
    blind_level = db.Column(db.String, nullable=False)

    player_states = db.relationship('PlayerState')
    table_state = db.relationship('TableState', uselist=False)

    create_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self):
        self.game_state = 0
        self.blind_level = 0
        self.player_states = []
        self.table_state = TableState()
        self.create_dttm = datetime.now()


    def as_dict(self):
        player_states_dict = [p.as_dict() for p in self.player_states]
        return {
            'ID': self.id,
            'GameState': self.game_state,
            'BlindLevel': self.blind_level,
            'PlayerStates': player_states_dict,
            'TableState': self.table_state.as_dict()
        }