from flask_marshmallow import Schema
from api import ma, TrainingModel

class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingModel
