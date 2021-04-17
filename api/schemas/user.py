from flask_marshmallow import Schema
from api import ma, UserModel
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
