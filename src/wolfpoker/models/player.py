from wolfpoker import db
from datetime import datetime
from ..models.player_state import PlayerState


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_guid = db.Column(db.Integer, db.ForeignKey('user.guid'))
    user = db.relationship('User', back_populates='players')
    game_guid = db.Column(db.Integer, db.ForeignKey('game.guid'))
    game = db.relationship('Game', back_populates='players')
    seat_id = db.Column(db.Integer, nullable=False)
    current_state = db.relationship(
        'PlayerState', uselist=False, back_populates='player')
    state_history = db.relationship('PlayerState')
    create_dttm = db.Column(db.DateTime, nullable=False)
    update_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self, stack, seat_id):
        self.current_state = PlayerState(stack)
        self.seat_id = seat_id


    def create(self):
        self.create_dttm = self.update_dttm = datetime.now()
        db.session.add(self)
        db.session.commit()
        self = self.fetch(name=self.name)
        return self


    @staticmethod
    def fetch(**kwargs):
        if 'id' in kwargs: return (
            Player.query.filter_by(id=int(kwargs['id'])).first())          
        elif 'name' in kwargs: return (
            Player.query.filter_by(name=kwargs['name']).first())
        return None


    @staticmethod
    def fetch_all():
        return Player.query.all()


    def as_dict(self):
        return (
            {
                'UserDetails': (
                    {
                        'GUID': self.user_guid,
                        'Username': self.user.username,
                        'ScreenName': self.user.screen_name
                    }),
                'GameGUID': self.game_guid,
                'State': current_state.as_dict()
            })