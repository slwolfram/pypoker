from pypoker import db


class PlayerState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Game', back_populates='player_state')
    stack = db.Column(db.Integer, nullable=False)
    hand = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    bet_amount = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    sitting_out = db.Column(db.Boolean, nullable=False)
    has_folded = db.Column(db.Boolean, nullable=False)
    is_winner = db.Column(db.Boolean, nullable=False)
    has_moved = db.Column(db.Boolean, nullable=False)
    entered_dttm = db.relationship(db.DateTime, nullable=False)