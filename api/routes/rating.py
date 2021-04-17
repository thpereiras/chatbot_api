import os
import sys
import datetime
from api import api, db, RatingResponseModel, RatingResponseSchema, RatingFinalModel, RatingFinalSchema
from flask import jsonify, request

@api.route("/rating/response", methods = ['POST'])
def create_rating_response():
    rating_schema = RatingResponseSchema()
    data = request.json

    session = data.get('session', '')
    question = data.get('question', '')
    answer = data.get('answer', '')
    helped = data.get('helped', '')
    timestamp = datetime.datetime.now()

    rating = RatingResponseModel(session = session, question = question, answer = answer, helped = helped, timestamp = timestamp)
    db.session.add(rating)
    db.session.commit()

    return rating_schema.jsonify(rating)
    return jsonify(message = "Rating created."), 200

@api.route("/rating/final", methods = ['POST'])
def create_rating_final():
    rating_schema = RatingFinalSchema()
    data = request.json

    session = data.get('session', '')
    rating_value = data.get('rating', '')
    timestamp = datetime.datetime.now()

    rating = RatingFinalModel(session = session, rating = rating_value, timestamp = timestamp)
    db.session.add(rating)
    db.session.commit()

    return rating_schema.jsonify(rating)
    return jsonify(message = "Rating created."), 200
