import datetime

from pypoker import db

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

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_seats': self.num_seats,
            'turn_time': self.turn_time,
            'blind_levels': self.blind_levels,
            'blind_length': self.blind_length,
            'buyin': self.buyin,
            'type': self.gtype,
            'start_time': (
                self.start_time.strftime("%m/%d/%Y, %H:%M:%S"))
        }