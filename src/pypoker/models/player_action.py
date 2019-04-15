from pypoker import db


class PlayerAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String, nullable=False)
    bet_amt = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='player_actions')
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.Column('Player', back_populates='player_actions')
    player_state_id = db.Column(
        db.Integer, db.ForeignKey('player_state.id'))
    player_state = db.Column(
        'PlayerState', back_populates='player_state')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.Column('Game', back_populates='player_actions')
    game_state_id = db.Column(
        db.Integer, db.ForeignKey('game_state.id'))
    game_state = db.Column('GameState', back_populates='game_state')
    action_dttm = db.Column(db.DateTime, nullable=False)