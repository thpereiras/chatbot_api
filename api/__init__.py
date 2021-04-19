import os
import sys
import pymysql
import logging
from chatterbot import ChatBot
from chatterbot import languages
from chatterbot.response_selection import get_random_response, get_first_response, get_most_frequent_response
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot import comparisons
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

logging.basicConfig(level=logging.INFO)

global chatbot
global default_response
global minimum_confidence

default_response = 'Desculpe, não entendi a sua pergunta.'
minimum_confidence = float(os.getenv('MINIMUM_CONFIDENCE', 0.6))

connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'], user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'], port=int(os.environ['MYSQL_PORT'])
)

with connection:
    with connection.cursor() as cursor:
        try:
            cursor.execute("DROP TABLE IF EXISTS {}".format("tag_association"))
            cursor.execute("DROP TABLE IF EXISTS {}".format("tag"))
            cursor.execute("DROP TABLE IF EXISTS {}".format("statement"))
        except:
            print('Tables not found', file=sys.stderr)

chatbot = ChatBot(
    "Nome do bot",
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    storage_adapter={
        'tagger_language': languages.POR,
        'import_path': 'chatterbot.storage.SQLStorageAdapter',
        'database_uri': "mysql+pymysql://"+os.environ['MYSQL_USER']+":"+os.environ['MYSQL_PASSWORD'] + \
        "@"+os.environ['MYSQL_HOST']+":"+"3306"+"/"+ \
        os.environ['MYSQL_DATABASE']+"?charset=utf8mb4",
    },
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': comparisons.LevenshteinDistance, # LevenshteinDistance, SpacySimilarity, JaccardSimilarity
            'response_selection_method': get_random_response,
            'default_response': default_response,
            'maximum_similarity_threshold': 0.95,
            'threshold': 0.75
        }
    ],
    read_only=True
)

api = Flask(__name__)
origins=os.environ['DOMAIN_WHITELIST'].split(',')
cors = CORS(api, resources={r"/*": {"origins": origins}})
cors = CORS(api, resources={r"/*": {"origins": "*"}})

bcrypt = Bcrypt(api)
jwt = JWTManager(api)

api.config.from_object('config')

ma = Marshmallow(api)
db = SQLAlchemy(api)

from .models.user import UserModel
from .models.training import TrainingModel
from .models.rating_final import RatingFinalModel
from .models.rating_response import RatingResponseModel
from .schemas.user import UserSchema
from .schemas.training import TrainingSchema
from .schemas.rating_final import RatingFinalSchema
from .schemas.rating_response import RatingResponseSchema

db.create_all()
db.session.commit()

@api.route("/restart")
@jwt_required()
def restart_chatbot():
    global chatbot

    connection = pymysql.connect(
        host=os.environ['MYSQL_HOST'], user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'], port=int(os.environ['MYSQL_PORT'])
    )
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                cursor.execute("TRUNCATE TABLE {}".format("tag"))
                cursor.execute(
                    "TRUNCATE TABLE {}".format("statement"))
                cursor.execute(
                    "TRUNCATE TABLE {}".format("tag_association"))
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            except error:
                print('Tables not found', file=sys.stderr)

    # Create a new trainer for the chatbot
    trainer = ChatterBotCorpusTrainer(chatbot, show_training_progress=True)

    trainer.train("./api/chatterbot-custom/greetings.yml")
    trainer.train("./api/chatterbot-custom/farewells.yml")
    trainer.train("./api/chatterbot-custom/thanks.yml")

    trainerList = ListTrainer(chatbot, show_training_progress=True)

    print('========================================================', file=sys.stderr)
    print('Selected language: ' + str(chatbot.storage.tagger.language.ENGLISH_NAME), file=sys.stderr)
    print('========================================================', file=sys.stderr)

    connection = pymysql.connect(
        host=os.environ['MYSQL_HOST'], user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'], port=int(os.environ['MYSQL_PORT'])
    )

    with connection:
        with connection.cursor() as cursor:
            result = cursor.execute("SELECT * FROM training")
            rows = cursor.fetchall()
            for row in rows:
                trainerList.train([row[1], row[2]])

    print('========================================================', file=sys.stderr)
    print('== Restart finished ====================================', file=sys.stderr)
    print('========================================================', file=sys.stderr)
    return jsonify(message="Chatbot API restarted"), 200

from .routes import auth
from .routes import rating
from .routes import admin
from .routes import chatterbot
from .resources.administration import Administration

Administration.create_admin_user(
    os.environ['ADMIN_NAME'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
