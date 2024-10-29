from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extension import db
from flask_login import UserMixin

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    weight_class = db.Column(db.String(32), nullable=False)
    team = db.Column(db.String(64), nullable=True)
    coach = db.Column(db.String(64), nullable=True)
    gender = db.Column(db.String(64), nullable=True)
    
    def __repr__(self):
        return f"Fighter {self.name} {self.surname} (ID: {self.id})"

class Fight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight_class = db.Column(db.String(32), nullable=False)
    red_corner = db.Column(db.String(128), nullable=True)
    blue_corner = db.Column(db.String(128), nullable=True)
    styles = db.Column(db.String(128), nullable=True)
    round = db.Column(db.String(128), nullable=True)
    time = db.Column(db.String(128), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='fights')

    def __repr__(self):
        return f"Fight {self.id} - {self.weight_class} - {self.red_corner} vs {self.blue_corner}"


class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fight_id = db.Column(db.Integer, db.ForeignKey('fight.id'), nullable=False)
    red_corner_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)
    blue_corner_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    red_corner = db.relationship('Fighter', foreign_keys=[red_corner_id], backref='fights_as_red')
    blue_corner = db.relationship('Fighter', foreign_keys=[blue_corner_id], backref='fights_as_blue')

    def __repr__(self):
        return f"Matchup: Fight ID {self.fight_id}, Red Corner: {self.red_corner.name}, Blue Corner: {self.blue_corner.name}"



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), index=True, unique=True)
    email = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    matchups = db.relationship('Matchup', backref='user', lazy='dynamic', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
