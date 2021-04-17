import os
import sys
from api import api, chatbot #, start_chatbot, start_flask
from flask import jsonify, request
from flask_jwt_extended import jwt_required

@api.route("/")
def home():
    return jsonify(message = "Bad request"), 400

@api.route('/api/talk', methods = ['POST'])
def talk():
    global chatbot
    content = request.json
    userText = content['message']

    userText = userText[:-1] if any(userText.endswith(x) for x in ('.','!',',',';','/','[',']','|','}','{')) else userText

    botResponse = str(chatbot.get_response(userText))
    print(userText, file=sys.stderr)
    print(botResponse, file=sys.stderr)
    return jsonify(response = botResponse), 200
