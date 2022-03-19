from werkzeug.exceptions import BadRequest

import app.tools.jwt_token as jwt
from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import Schema, fields, ValidationError

from app.container import user_service
from app.exceptions import DuplicateError

auth_ns = Namespace('auth')


class LoginValidator(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterValidator(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre_id = fields.Int()


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        """Create token"""
        try:
            validated_data = LoginValidator().load(request.json)
            user = user_service.get_by_email(validated_data['email'])
            if not user:
                print("None email")
                abort(404)

            token_data = jwt.JwtSchema().load({'user_id': user.id}) # , 'role': user.role_id
            return jwt.JwtToken(token_data).get_tokens(), 201

        except ValidationError:
            abort(400)

    def put(self):
        """Update token"""
        try:
            r_token = request.json.get('refresh_token')
            data = jwt.JwtToken.decode_token(r_token)
            if not data:
                abort(404)

            token_data = jwt.JwtSchema().load({'user_id': data['user_id'], 'exp': data['exp']}) # , 'role': data['role']
            return jwt.JwtToken(token_data).get_tokens(), 201

        except ValidationError as e:
            print(str(e))
            abort(400)


@auth_ns.route('/register')
class AuthRegisterView(Resource):

    def post(self):
        """ Create user """
        try:
            user = user_service.create_alternative(**RegisterValidator().load(request.json)) # create_alternative
            return f'User {user} created'
        except ValidationError:
            raise BadRequest
        except DuplicateError:
            return 'Username already exists', 404


