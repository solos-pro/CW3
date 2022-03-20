from flask import request, json
from flask_restx import Resource, Namespace
from marshmallow import ValidationError, Schema, fields
from werkzeug.exceptions import BadRequest

from app.container import user_service
from app.model.user import UserSchema
from app.views.auth import LoginValidator
from app.exceptions import DuplicateError
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


@user_ns.route('/') # <int:uid>
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
        # return validated_data, 200 #


    # def post(self):
    #     """ Create user """
    #     try:
    #         user_service.create(**LoginValidator().load(request.json))
    #     except ValidationError:
    #         raise BadRequest
    #     except DuplicateError:
    #         raise BadRequest('Username already exists')


# @user_ns.route('/option/') # <int:uid>
# class UserView(Resource):
#
#     def post(self):
#         """ Create user """
#         try:
#             user = user_service.create_alternative(**LoginValidator().load(request.json)) # create_alternative
#             return f'User {user} created'
#         except ValidationError:
#             raise BadRequest
#         except DuplicateError:
#             return 'Username already exists', 404
