from flask import request
from flask_restx import Resource, Namespace
from marshmallow import Schema, fields

from app.container import user_service
from app.model.user import UserSchema
from app.tools.auth import login_required

user_ns = Namespace('users')
user_schema = UserSchema()


class PachUserValidator(Schema):
    name = fields.Str()
    surname = fields.Str()
    favorite_genre_id = fields.Int()


class PassUpdateValidator(Schema):
    password_1 = fields.Str(required=True)
    password_2 = fields.Str(required=True)


@user_ns.route('/')
class UserView(Resource):
    @login_required
    def get(self, token_data):
        user = user_service.get_one(token_data['user_id'])
        if not user:
            return "", 404
        return user_schema.dump(user)

    @login_required
    def patch(self, token_data):
        validated_data = PachUserValidator().load(request.json)
        user = user_service.get_one(token_data['user_id'])
        if not user:
            return "", 404
        result = user_service.update_partial(validated_data, token_data['user_id']) #
        return user_schema.dump(result), 200 # , validated_data


@user_ns.route('/password')
class UserPasswView(Resource):
    @login_required
    def put(self, token_data):
        validated_data = PassUpdateValidator().load(request.json)
        user = user_service.get_one(token_data['user_id'])
        print(validated_data, "- validated_data")
        if not user:
            return "", 404
        compare_passwords_OK = user_service.compare_password(validated_data, token_data['user_id']) #
        if not compare_passwords_OK:
            return "permission denied", 401
        if compare_passwords_OK:
            result = user_service.update_password(validated_data, token_data['user_id'])
        return user_schema.dump(result), 200 #


