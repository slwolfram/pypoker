from pypoker import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    stack = db.Column(db.Integer, nullable=False)
    hand = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    bet_amount = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    has_folded = db.Column(db.Boolean, nullable=False)
    is_winner = db.Column(db.Boolean, nullable=False)
    has_moved = db.Column(db.Boolean, nullable=False)

    def __str__(self):
        return "name:{} cash:{} hand:{} position:{}".format(
            self.name, self.cash, self.hand, self.position)

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cash': self.cash,
            'hand': self.hand,
            'position': self.position,
            'bet_amount': self.bet_amount,
            'is_active': self.is_active,
            'has_folded': self.has_folded,
            'is_winner': self.is_winner,
            'has_moved': self.has_moved
        }
