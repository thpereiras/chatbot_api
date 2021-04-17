import os
import random
import string
from datetime import timedelta

basedir = os.path.dirname(os.path.realpath(__file__))

user = os.environ['MYSQL_USER']
passwd = os.environ['MYSQL_PASSWORD']
database = os.environ['MYSQL_DATABASE']
host = os.environ['MYSQL_HOST']
port = int(os.environ.get("MYSQL_PORT", 3306))

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(
    os.environ['JWT_ACCESS_TOKEN_EXPIRES_MINUTES']))

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 120,
    'pool_pre_ping': True
}
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ['DEBUG']
