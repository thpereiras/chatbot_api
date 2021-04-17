import os
import sys
import datetime
from api import api, chatbot, db, UserModel
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

@api.route('/api/login', methods = ['POST'])
def login():
    content = request.json
    if not {'login', 'password'} <= set(content):
      return {'error': 'Credential not sent'}, 401

    user = UserModel.query.filter_by(login=content['login']).first()
    if not user:
      return {'error': 'Email or password invalid'}, 401

    authorized = user.check_password(content['password'])
    if not authorized:
        return {'error': 'Email or password invalid'}, 401

    expires = datetime.timedelta(days=1)
    access_token = create_access_token(
        identity=str(user.id), expires_delta=None)
    return {'token': access_token, 'name': user.name }, 200

@api.route('/api/ping', methods = ['GET'])
@jwt_required()
def ping():
    return '', 200
