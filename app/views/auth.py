import app.tools.jwt_token as jwt
from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import Schema, fields, ValidationError

from app.container import user_service

auth_ns = Namespace('auth')


class LoginValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str()


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        """Create token"""
        try:
            validated_data = LoginValidator().load(request.json)
            user = user_service.get_by_username(validated_data['username'])
            if not user:
                print("None user")
                abort(404)

            token_data = jwt.JwtSchema().load({'user_id': user.id, 'role': user.role_id})
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

            token_data = jwt.JwtSchema().load({'user_id': data['user_id'], 'role': data['role'], 'exp': data['exp']}) #
            return jwt.JwtToken(token_data).get_tokens(), 201

        except ValidationError as e:
            print(str(e))
            abort(400)
