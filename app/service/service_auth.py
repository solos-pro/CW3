import base64
import hashlib
import hmac
import datetime
import calendar
import jwt
from flask import request, abort
from app.service.service_user import UserService
# from app.container import user_service
from app.tools.jwt_token import JwtToken
from app.tools.security import compare_passwords
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, PWD_HASH_ALGO, SECRET


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def validate_jwt_generate(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)
        if user is None:
            raise abort(404)
        if not is_refresh:
            if not compare_passwords(user.password, password):
                abort(401)

        return generate_jwt(user)


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, SECRET, algorithms=[PWD_HASH_ALGO])
            role = user.get("role")
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        if role != "admin":
            abort(403)
        return func(*args, **kwargs)

    return wrapper


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, SECRET, algorithms=[PWD_HASH_ALGO])
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)
        return func(*args, **kwargs)

    return wrapper

'''
def hash_encode(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )  # .decode("utf-8", "ignore")


def hash_str_encode(data):
    return base64.b64encode(data)


def compare_passwords(password_hash, other_password):
    decoded_digest = base64.decode(password_hash)
    return hmac.compare_digest(decoded_digest, hash_encode(other_password))
'''

def generate_jwt(user_obj):
    data = {
        "username": user_obj.get('username'),
        "role": user_obj.get('role')
    }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET, algorithm=PWD_HASH_ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET, algorithm=PWD_HASH_ALGO)

    return {"access_token": access_token, "refresh_token": refresh_token}
