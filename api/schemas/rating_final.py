from flask_marshmallow import Schema
from api import ma, RatingFinalModel

class RatingFinalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RatingFinalModel
