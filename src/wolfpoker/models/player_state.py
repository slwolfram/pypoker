from wolfpoker import db


class PlayerState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_state_id = db.Column(db.Integer, db.ForeignKey('game_state.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship(
        'Player', back_populates='current_state')
    player_action = db.relationship('PlayerAction', uselist=False)
    stack = db.Column(db.Float, nullable=False)
    hand = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    bet_total = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    sitting_out = db.Column(db.Boolean, nullable=False)
    has_folded = db.Column(db.Boolean, nullable=False)
    is_winner = db.Column(db.Boolean, nullable=False)
    has_moved = db.Column(db.Boolean, nullable=False)
    create_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self, stack):
        self.stack = stack
        self.hand = ""
        self.position = -1
        self.bet_total = 0
        self.is_active = self.sitting_out = self.has_folded \
                       = self.is_winner = self.has_moved = False


    def as_dict(self):
        return (
            {
                'Action': self.player_action.as_dict(),
                'Stack': self.stack,
                'Hand': self.hand,
                'Position': self.position,
                'BetTotal': self.bet_total,
                'IsActive': self.is_active,
                'SittingOut': self.sitting_out,
                'HasFolded': self.has_folded,
                'IsWinner': self.is_winner,
                'HasMoved': self.has_moved,
                'CreateDTTM': self.create_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S")
            })


    def long_dict(self):
        d = self.as_dict()
        d['PlayerDetails'] = (
            {
                'GameGUID': self.player.game_guid,
                'UserGUID': self.player.user_guid,
                'ScreenName': self.player.user.screen_name,
                'Username': self.player.user.username,
                'CreateDTTM': self.player.create_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S"),
                'UpdateDTTM': self.player.update_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S")
            })
        return d


    def make_copy(self):
        cpy = PlayerState(self.stack)
        cpy.hand = self.hand
        cpy.position = self.position
        cpy.bet_total = self.bet_total
        cpy.is_active = self.is_active
        cpy.sitting_out = self.sitting_out
        cpy.has_folded = self.is_folded
        cpy.is_winner = self.is_winner
        cpy.has_moved = self.has_moved
        
