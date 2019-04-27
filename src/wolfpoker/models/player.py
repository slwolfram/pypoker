from wolfpoker import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='players')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', back_populates='players')
    player_state_current = db.relationship(
        'PlayerState', uselist=False, back_populates='player')
    player_state_history = db.relationship('PlayerState')
    create_dttm = db.Column(db.DateTime, nullable=False)
    update_dttm = db.Column(db.DateTime, nullable=False)
    

    def __str__(self):
        return "name:{} cash:{} hand:{} position:{}".format(
            self.name, self.cash, self.hand, self.position)


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