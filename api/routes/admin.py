import os
import sys
import datetime
from math import ceil
from api import api, db, RatingResponseModel, RatingResponseSchema, RatingFinalModel, RatingFinalSchema, TrainingModel, TrainingSchema
from flask import jsonify, request
from flask_jwt_extended import jwt_required

# Retorna os pares de pergunta e resposta e sua avaliação.
@api.route("/rating/response", methods=['GET'])
@api.route("/rating/response/<int:page>", methods=['GET'])
@jwt_required()
def get_rating_response(page=1):
    per_page = 5000
    rating_response_schema = RatingResponseSchema(many=True)
    all_responses = RatingResponseModel.query.order_by(RatingResponseModel.id.asc(
    ), RatingResponseModel.session.asc()).paginate(page, per_page, error_out=False)
    total_pages = ceil(all_responses.total / all_responses.per_page)
    result = jsonify(
        data=rating_response_schema.dump(all_responses.items),
        pagination={"page": all_responses.page, "per_page": all_responses.per_page,
                    "total_pages": total_pages,  "total": all_responses.total}
    )
    return result

# Apaga um pare de pergunta e resposta e sua avaliação.
@api.route("/rating/response/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_rating_response(id):
    try:
        rating_response = RatingResponseModel.query.get(id)
        db.session.delete(rating_response)
        db.session.commit()
        return '', 204
    except:
        return '', 204

# Retorna a lista de avaliações finais.
@api.route("/rating/final", methods=['GET'])
@api.route("/rating/final/<int:page>", methods=['GET'])
@jwt_required()
def get_rating_final(page=1):
    per_page = 5000
    rating_final_schema = RatingFinalSchema(many=True)
    all_finals = RatingFinalModel.query.order_by(
        RatingFinalModel.id.asc()).paginate(page, per_page, error_out=False)
    total_pages = ceil(all_finals.total / all_finals.per_page)
    result = jsonify(
        data=rating_final_schema.dump(all_finals.items),
        pagination={"page": all_finals.page, "per_page": all_finals.per_page,
                    "total_pages": total_pages, "total": all_finals.total}
    )
    return result

# Apaga uma avaliação final.
@api.route("/rating/final/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_rating_final(id):
    try:
        rating_final = RatingFinalModel.query.get(id)
        db.session.delete(rating_final)
        db.session.commit()
        return '', 204
    except:
        return '', 204

# Retorna os pares de pergunta e resposta de treinamento
@api.route("/training", methods=['GET'])
@api.route("/training/<int:page>", methods=['GET'])
@jwt_required()
def get_training(page=1):
    per_page = 5000
    training_schema = TrainingSchema(many=True)
    all_training = TrainingModel.query.order_by(
        TrainingModel.id.asc()).paginate(page, per_page, error_out=False)
    total_pages = ceil(all_training.total / all_training.per_page)
    result = jsonify(
        data=training_schema.dump(all_training.items),
        pagination={"page": all_training.page, "per_page": all_training.per_page,
                    "total_pages": total_pages,  "total": all_training.total}
    )
    return result

# Apaga um pare de pergunta e resposta e sua avaliação.
@api.route("/training/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_training(id):
    try:
        training = TrainingModel.query.get(id)
        db.session.delete(training)
        db.session.commit()
        return '', 204
    except:
        return '', 204

@api.route("/training/create", methods = ['POST'])
def create_treianin():
    training_schema = TrainingSchema()
    data = request.json

    if not data.get('questions', '') or not data.get('answer', ''):
        return {'error': 'Question or naswer invalid'}, 400

    for q in data.get('questions', ''):
        question = q
        if q == '':
          continue
        answer = data.get('answer', '')
        timestamp = datetime.datetime.now()
        training = TrainingModel(question = question, answer = answer, timestamp = timestamp)
        db.session.add(training)
        db.session.commit()

    return {'success': True}, 201
