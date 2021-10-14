from app import db, login_manager
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, email, name, phone, password):
        self.username = username
        self.email = email
        self.name = name
        self.phone = phone
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
        