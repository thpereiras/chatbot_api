import os
import sys
from api import api, chatbot, default_response, minimum_confidence
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
    botResponse = chatbot.get_response(userText)

    if float(botResponse.confidence) > minimum_confidence:
        return jsonify(response = str(botResponse)), 200
    else:
        return jsonify(response = default_response), 200
