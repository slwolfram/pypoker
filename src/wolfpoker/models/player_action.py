from wolfpoker import db


class PlayerAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action_cd = db.Column(db.String, nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    player_state_id = db.Column(
        db.Integer, db.ForeignKey('player_state.id'))  
    create_dttm = db.Column(db.DateTime, nullable=False)


    def as_dict(self):
        return {
            'Action': self.action_cd,
            'BetAmount': self.bet_amount,
            'CreateDTTM': self.create_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S")
        }