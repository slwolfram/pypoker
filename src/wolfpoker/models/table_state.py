from datetime import datetime
from ..helper.deck import Deck
from wolfpoker import db


class TableState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_state_id = db.Column(db.Integer, db.ForeignKey('game_state.id'))
    pot = db.Column(db.Float, nullable=False)
    deck = db.Column(db.String, nullable=False)
    board = db.Column(db.String, nullable=False)
    create_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self):
        self.pot = 0
        self.deck = str(Deck())
        self.board = ""


    def as_dict(self):
        return (
            {
                'Pot': self.pot,
                'Deck': self.deck,
                'Board': self.board
            })


    def make_copy(self):
        cpy = TableState()
        cpy.pot = self.pot
        cpy.deck = self.deck
        cpy.board = self.board
