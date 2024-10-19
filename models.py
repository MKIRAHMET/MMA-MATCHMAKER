from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Fighters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    weight_class = db.Column(db.String(32), nullable=False)
    team = db.Column(db.String(64), nullable=True)
    coach = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return f"Fighter {self.name} {self.surname} (ID: {self.id})"

class FightItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fight_id = db.Column(db.Integer, db.ForeignKey('fights.id'), nullable=False)
    red_corner_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=False)
    blue_corner_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=False)

    red_corner = db.relationship('Fighters', foreign_keys=[red_corner_id], backref='fights_as_red')
    blue_corner = db.relationship('Fighters', foreign_keys=[blue_corner_id], backref='fights_as_blue')

    def __repr__(self):
        return f"FightItem: Fight ID {self.fight_id}, Red Corner ID {self.red_corner_id}, Blue Corner ID {self.blue_corner_id}"

class Fights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)  # Optional date field
    location = db.Column(db.String(128), nullable=True)  # Optional location field
    items = db.relationship('FightItem', backref='fight', lazy='dynamic', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f"Fight {self.id} - {self.location or 'Location Unknown'}"
