from pypoker import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    stack = db.Column(db.Integer, nullable=False)
    hand = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    bet_amount = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    sitting_out = db.Column(db.Boolean, nullable=False)
    has_folded = db.Column(db.Boolean, nullable=False)
    is_winner = db.Column(db.Boolean, nullable=False)
    has_moved = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='players')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', back_populates='players')


    def __str__(self):
        return "name:{} cash:{} hand:{} position:{}".format(
            self.name, self.cash, self.hand, self.position)


    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cash': self.cash,
            'hand': self.hand,
            'position': self.position,
            'bet_amount': self.bet_amount,
            'is_active': self.is_active,
            'sitting_out': self.sitting_out,
            'has_folded': self.has_folded,
            'is_winner': self.is_winner,
            'has_moved': self.has_moved
        }

    def create(self):
        try:
            db.create_all()
            db.session.add(self)
            db.session.commit()
            self = self.fetch(name=self.name)
        except Exception as e:
            print(repr(e))
            return -1
        return self

    @staticmethod
    def fetch(**kwargs):
        player = None
        try:
            if 'id' in kwargs:
                player = Player.query.filter_by(
                    id=int(kwargs['id'])).first()            
            elif 'name' in kwargs:
                player = Player.query.filter_by(
                    name=kwargs['name']).first()
        except:
            return -1
        return player


    @staticmethod
    def fetch_all():
        try:
            players = Player.query.all()
        except:
            return -1
        return players