from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from app.container import user_service
from app.model.user import UserSchema
from app.views.auth import LoginValidator
from app.exceptions import DuplicateError
from app.tools.auth import login_required

user_ns = Namespace('users')
user_schema = UserSchema()


@user_ns.route('/') # <int:uid>
class UserView(Resource):
    @login_required
    def get(self, token_data):
        print(token_data)
        user = user_service.get_one(token_data['user_id'])
        if not user:
            return "", 404
        return user_schema.dump(user)

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
