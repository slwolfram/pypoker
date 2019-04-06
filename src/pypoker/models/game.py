import datetime

from pypoker import db
from pypoker.deck import Deck


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    turn_time = db.Column(db.Integer, nullable=False)
    blind_levels = db.Column(db.String, nullable=False)
    blind_length = db.Column(db.String, nullable=False)
    buyin = db.Column(db.String, nullable=False)
    gtype = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    deck = db.Column(db.String, nullable=False)
    players = db.relationship('Player', back_populates='game')



    def as_dict(self):
        return {
            'ID': self.id,
            'Name': self.name,
            'NumSeats': self.num_seats,
            'TurnTime': self.turn_time,
            'BlindLevels': self.blind_levels,
            'BlindLength': self.blind_length,
            'Buyin': self.buyin,
            'Type': self.gtype,
            'StartTime': (
                self.start_time.strftime("%m/%d/%Y, %H:%M:%S"))
        }


    def create(self):
        self.deck = str(Deck())
        print(self.deck)
        try:
            db.create_all()
            db.session.add(self)
            db.session.commit()
            self = self.fetch(name=self.name)
            return self
        except Exception as e:
            print(repr(e))
        return None


    @staticmethod
    def fetch(**kwargs):
        try:
            if 'id' in kwargs:
                return Game.query.filter_by(
                    id=int(kwargs['id'])).first()            
            elif 'name' in kwargs:
                return Game.query.filter_by(
                    name=kwargs['name']).first()
        except:
            pass
        return None


    @staticmethod
    def fetch_all():
        try:
            return Game.query.all()
        except:
            pass
        return None