from api import db
from flask_bcrypt import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)

    def __init__(self, name, login, password, timestamp):
        self.name = name
        self.login = login
        self.password = generate_password_hash(password).decode('utf8')
        self.timestamp = timestamp

    def check_password(self, password):
      return check_password_hash(self.password, password)
