from flask_marshmallow import Schema
from api import ma, RatingResponseModel

class RatingResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RatingResponseModel
