import datetime

from pypoker import db
from pypoker.deck import Deck


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    turn_time = db.Column(db.Integer, nullable=False)
    blinds = db.Column(db.String, nullable=False)
    blind_level = db.Column(db.Integer, nullable=False)
    blind_length = db.Column(db.String, nullable=False)
    buyin = db.Column(db.String, nullable=False)
    gtype = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    deck = db.Column(db.String, nullable=False)
    players = db.relationship('Player', back_populates='game')

    def get_blinds(self):
        blinds = self.blinds.split('|')
        blinds = blinds[self.blind_level]
        blinds = blinds.split(',')
        return list(map(int, blinds))

    def get_buyin(self):
        buyin = ["",""] if self.buyin == "" else self.buyin.split('-')
        return buyin

    def as_dict(self):
        player_dict = []
        for p in self.players:
            player_dict.append(p.as_dict())
        return {
            'ID': self.id,
            'Name': self.name,
            'NumSeats': self.num_seats,
            'TurnTime': self.turn_time,
            'Blinds': self.get_blinds(),
            'Buyin': self.get_buyin(),
            'GameType': self.gtype,
            'StartTime': (
                self.start_time.strftime("%m/%d/%Y, %H:%M:%S")),
            'Players': player_dict
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