from itsdangerous import (TimedJSONWebSignatureSerializer 
    as Serializer, BadSignature, SignatureExpired)
from flask import current_app
from passlib.apps import custom_app_context as pwd_context

from pypoker import db
from pypoker.apis.validation.response import bad_request, good_request


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String)
    bankroll = db.Column(db.Integer, nullable=False)
    players = db.relationship("Player", back_populates="user")

    def generate_auth_token(self, expiration=6000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return str(s.dumps({'id': self.id}))

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return bad_request('Authentication token has expired', 401)
        except BadSignature:
            return bad_request('Invalid authentication token', 401)
        user = User.query.get(data['id'])
        return good_request(user.as_dict(), 200)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nickname': self.nickname,
            'bankroll': self.bankroll
        }

    def create(self):
        try:
            db.create_all()
            db.session.add(self)
            db.session.commit()
            self = self.fetch(username=self.username)
            return self
        except:
            pass
        return None

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
            pass
        return None

    @staticmethod
    def fetch_all():
        try:
            return User.query.all()
        except:
            pass
        return None