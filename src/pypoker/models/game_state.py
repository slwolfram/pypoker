from pypoker import db


class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # game
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', back_populates='game_state')
    # active player
    active_player_state_id = db.Column(
        db.Integer, ForeignKey('player_state.id'))
    active_player_state = db.relationship(
        'PlayerState', back_populates='game_state')
    # active player action
    active_player_action_id = db.Column(
        db.Integer, ForeignKey('active_player.id'))
    active_player_action = db.relationship(
        'PlayerAction', back_populates='game_state')
    # game state
    game_round = db.Column(db.String, nullable=False)
    blind_state = db.Column(db.String, nullable=False)
    deck_state = db.Column(db.String, nullable=False)
    player_states = db.relationship(
        'PlayerState', back_populates='game_state')
    board_state = db.Column(db.String, nullable=False)
    entered_dttm = db.Column(db.DateTime, nullable=False)
