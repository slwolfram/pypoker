from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer 
    as Serializer, BadSignature, SignatureExpired)
from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from pypoker import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    screen_name = db.Column(db.String, nullable=False)
    bankroll = db.Column(db.Float, nullable=False)
    players = db.relationship('Player', back_populates='user')

    create_dttm = db.Column(db.DateTime, nullable=False)
    update_dttm = db.Column(db.DateTime, nullable=False)


    def __init__(self, username, password, email, **kwargs):
        self.username = username
        self.hash_password(password)
        self.email = email
        self.screen_name = kwargs['screen_name'] \
            if 'screen_name' in kwargs else ''
        self.bankroll = 0


    def generate_auth_token(self, expiration=6000):
        s = Serializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        token = str(s.dumps({'id': self.id}))
        token = token.replace("b'", "")
        token = token.replace("'", "")
        return token


    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        user = User.query.get(data['id'])
        return user


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)


    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


    def as_dict(self):
        return {
            'ID': self.id,
            'Username': self.username,
            'Email': self.email,
            'ScreenName': self.screen_name,
            'Bankroll': self.bankroll,
            'CreateDTTM': self.create_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S"),
            'UpdateDTTM': self.update_dttm
                              .strftime("%m/%d/%Y, %H:%M:%S")
        }


    def create(self):
        self.create_dttm = self.update_dttm = datetime.now()
        try:
            db.create_all()
            db.session.add(self)
            db.session.commit()
            self = self.fetch(username=self.username)
        except:
            return None
        return self


    @staticmethod
    def fetch(**kwargs):
        try:
            if 'id' in kwargs:
                return User.query.filter_by(
                    id=int(kwargs['id'])).first()            
            elif 'email' in kwargs:
                return User.query.filter_by(
                    email=kwargs['email']).first()
            elif 'username' in kwargs:
                return User.query.filter_by(
                    username=kwargs['username']).first()
        except:
            return -1
        return None


    @staticmethod
    def fetch_all():
        try:
            return User.query.all()
        except:
            return -1
        return None