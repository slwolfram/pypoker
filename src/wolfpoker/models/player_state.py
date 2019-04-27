from wolfpoker import db


class PlayerState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_state_id = db.Column(db.Integer, db.ForeignKey('game_state.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship(
        'Player', back_populates='player_state_current')
    player_action = db.relationship('PlayerAction', uselist=False)
    stack = db.Column(db.Float, nullable=False)
    hand = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    bet_amt_total = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    sitting_out = db.Column(db.Boolean, nullable=False)
    has_folded = db.Column(db.Boolean, nullable=False)
    is_winner = db.Column(db.Boolean, nullable=False)
    has_moved = db.Column(db.Boolean, nullable=False)
    create_dttm = db.Column(db.DateTime, nullable=False)


    def as_dict(self):
        return {
            'ID': self.id,
            'PlayerDetails': {
                'PlayerID': self.player.id,
                'UserID': self.player.user.id,
                'ScreenName': self.player.user.screen_name,
                'CreateDTTM': self.player.create_dttm
                                  .strftime("%m/%d/%Y, %H:%M:%S"),
                'UpdateDTTM': self.player.update_dttm
                                  .strftime("%m/%d/%Y, %H:%M:%S")
            },
            'Stack': self.stack,
            'Hand': self.hand,
            'Position': self.position,
            'BetAmtTotal': self.bet_amt_total,
            'IsActive': self.is_active,
            'SittingOut': self.sitting_out,
            'HasFolded': self.has_folded,
            'IsWinner': self.is_winner,
            'HasMoved': self.has_moved,
            'CreateDTTM': self.create_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S")
        }
        
