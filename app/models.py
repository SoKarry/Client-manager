from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    comp_name = db.Column(db.String(60))
    comp_bill = db.Column(db.Integer())
    bank_name = db.Column(db.String())
    cor_bill = db.Column(db.Integer())
    INN = db.Column(db.Integer())
    KPP = db.Column(db.Integer())
    BIK = db.Column(db.Integer())
    default_delivery = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    leads = db.relationship('Lead', backref='author', lazy='dynamic')
    tovars = db.relationship('Tovar', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    fio = db.Column(db.String(90))
    tovar = db.Column(db.String(140))
    price = db.Column(db.Float)
    contact = db.Column(db.String(90))
    address = db.Column(db.String(140))
    cost_price = db.Column(db.Float)
    delivery_price = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float)
    track = db.Column(db.String(20))
    status = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Lead {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(self.timestamp, self.fio, self.tovar, self.price, self.contact, self.address, self.cost_price, self.profit, self.track, self.status)

class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tovar_name = db.Column(db.String(140))
    tovar_cost_price = db.Column(db.Float)
    tovar_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Lead {}, {}, {}>'.format(self.tovar_name, self.tovar_cost_price, self.tovar_price)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))