from datetime import datetime
from wolfpoker import db
from ..models.table_state import TableState


class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship(
        'Game', back_populates='current_state')
    # -1 - Waiting to start
    #  0 - Round reset
    #  1 - Preflop
    #  2 - Flop
    #  3 - Turn
    #  4 - River
    #  5 - Evaluating hands
    #  6 - Distribute winnings
    game_state_cd = db.Column(db.Integer, nullable=False)
    blind_level = db.Column(db.String, nullable=False)
    player_states = db.relationship('PlayerState')
    table_state = db.relationship('TableState', uselist=False)
    create_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self):
        self.game_state_cd = 0
        self.blind_level = 0
        self.player_states = []
        self.table_state = TableState()


    def __get_state_string(self):
        if   self.game_state_cd ==-1: return 'WAITING TO START'
        elif self.game_state_cd == 0: return 'ROUND RESET'
        elif self.game_state_cd == 1: return 'PREFLOP'
        elif self.game_state_cd == 2: return 'FLOP'
        elif self.game_state_cd == 3: return 'TURN'
        elif self.game_state_cd == 4: return 'RIVER'
        elif self.game_state_cd == 5: return 'EVALUATING HANDS'
        elif self.game_state_cd == 6: return 'DISTRIBUTE WINNINGS'
        else:                    return 'ERROR'


    def as_dict(self):
        player_states_dict = [p.as_dict() for p in self.player_states]
        return (
            {
                'GameState': self.__get_state_string(),
                'BlindLevel': self.blind_level,
                'PlayerStates': player_states_dict,
                'TableState': self.table_state.as_dict()
            })


    def make_copy(self):
        cpy = GameState()
        cpy.game_state_cd = self.game_state_cd
        cpy.blind_level = self.blind_level
        cpy.table_state = self.table_state
        cpy.player_states = self.player_states
        return cpy

