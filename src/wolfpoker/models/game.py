from uuid import uuid4
from datetime import datetime

from wolfpoker import db
from ..helper.deck import Deck
from ..models.game_state import GameState
from ..models.player import Player


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


    def new_state(self):
        self.state_history.append(self.current_state)
        self.current_state = self.current_state.make_copy()


    def join(self, user, stack, **kwargs):
        seat_id = kwargs['seat_id'] if 'seat_id' in kwargs else None
        if len(self.players) == self.num_seats: 
            return None
        if seat_id:
            if seat_id < len(self.players) and \
                any(p.seat_id == seat_id \
                or p.user_guid == user.guid \
                for p in self.players): return None
        else: 
            for i in range(self.num_seats):
                if not any(p.seat_id == i for p in self.players):
                    seat_id = i
        self.new_state()
        user.bankroll -= stack
        player = Player(stack, seat_id)
        user.players.append(player)
        self.players.append(player)
        self.current_state.player_states.append(player.current_state)
        db.session.commit()
        return Player.fetch(
            user_guid=self.user_guid, game_guid=self.game_guid)