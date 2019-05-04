from uuid import uuid4
from datetime import datetime

from wolfpoker import db
from ..helper.deck import Deck
from ..models.game_state import GameState


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    turn_time = db.Column(db.Integer, nullable=False)
    blinds = db.Column(db.String, nullable=False)
    blind_length = db.Column(db.String, nullable=False)
    buyin = db.Column(db.String, nullable=False)
    game_type = db.Column(db.String, nullable=False)
    game_format = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    players = db.relationship('Player', back_populates='game')
    current_state = db.relationship(
        'GameState', uselist=False, back_populates='game')
    state_history = db.relationship('GameState')
    create_dttm = db.Column(db.DateTime, nullable=False)
    update_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self, name, num_seats, turn_time, blinds, 
                 blind_length, buyin, game_type, game_format, 
                                                 start_time):
        self.name = name
        self.num_seats = num_seats
        self.turn_time = turn_time
        self.blinds = blinds
        self.blind_length = blind_length
        self.buyin = buyin
        self.game_type = game_type
        self.game_format = game_format
        self.start_time = start_time
        self.guid = str(uuid4().hex)
        self.current_state = GameState()


    def create(self):
        self.create_dttm = \
            self.update_dttm = self.current_state.create_dttm = \
            self.current_state.table_state.create_dttm = datetime.now()
        db.session.add(self)
        db.session.commit()
        self = self.fetch(guid=self.guid)
        return self


    @staticmethod
    def fetch(**kwargs):
        if 'id' in kwargs: return (
            Game.query.filter_by(id=int(kwargs['id'])).first())           
        elif 'guid' in kwargs: return (
            Game.query.filter_by(guid=kwargs['guid']).first())
        return None


    @staticmethod
    def fetch_all():
        return Game.query.all()


    def get_buyin(self):
        buyin = ["",""] if self.buyin == "" else self.buyin.split('-')
        return buyin


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def as_dict(self):
        player_dict = [p.as_dict() for p in self.players]
        game_state_dict = self.current_state.as_dict()
        return (
            {
                'GUID': self.guid,
                'Name': self.name,
                'NumSeats': self.num_seats,
                'TurnTime': self.turn_time,
                'Blinds': self.blinds.split('|'),
                'Buyin': self.get_buyin(),
                'GameType': self.game_type,
                'GameFormat': self.game_format,
                'Players': player_dict,
                'StartTime': (
                    self.start_time.strftime("%m/%d/%Y, %H:%M:%S")),
                'GameState': game_state_dict,
                'UpdateDTTM': (
                    self.update_dttm.strftime("%m/%d/%Y, %H:%M:%S"))
            })