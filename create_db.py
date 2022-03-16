# Это файл конфигурации приложения, здесь может храниться путь к БД, ключ шифрования, что-то еще.
# Чтобы добавить новую настройку, допишите ее в класс.
import base64
import hashlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from constants import PWD_HASH_ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET

# from app.dao.model.director import Director
# from app.dao.model.genre import Genre
# from app.dao.model.movie import Movie
import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship('Genre')
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    director = db.relationship('Director')


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), unique=True)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    role = db.relationship("Group")


db.drop_all()
db.create_all()


# ---------------------------------------

def get_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name=PWD_HASH_ALGO,
        password=password.encode("utf-8"),
        salt=PWD_HASH_SALT,
        iterations=PWD_HASH_ITERATIONS
    )


def get_password_hash(password: str) -> str:
    return base64.b64encode(get_password_digest(password)).decode('utf-8', "ignore")


# ---------------------------------------

# def get_hash(password):
#     result = hashlib.pbkdf2_hmac(
#         PWD_HASH_ALGO,
#         password.encode('utf-8'),
#         PWD_HASH_SALT,
#         PWD_HASH_ITERATIONS
#     )
#     return base64.b64encode(result)


for role in raw_data.roles:
    data = Group(
        role=role["role"]
    )

    with db.session.begin():
        db.session.add(data)

for user in raw_data.users:
    password = user["password"]

    data = User(
        username=user["username"],
        role_id=user["role_id"],
        password=get_password_hash(user["password"])
    )

    with db.session.begin():
        db.session.add(data)

for director in raw_data.directors:
    d = Director(
        id=director["pk"],
        name=director["name"]
    )
    with db.session.begin():
        db.session.add(d)

for genre in raw_data.genres:
    d = Genre(
        id=genre["pk"],
        name=genre["name"]
    )
    with db.session.begin():
        db.session.add(d)

for movie in raw_data.movies:
    m = Movie(
        id=movie["pk"],
        title=movie["title"],
        description=movie["description"],
        trailer=movie["trailer"],
        year=movie["year"],
        rating=movie["rating"],
        genre_id=movie["genre_id"],
        director_id=movie["director_id"]
    )

    with db.session.begin():
        db.session.add(m)

# u1 = User(username="vasya", password="my_little_pony", role="user")
# u2 = User(username="oleg", password="qwerty", role="user")
# u3 = User(username="oleg", password="P@ssw0rd", role="admin")
#
# with db.session.begin():
#     db.session.add(u1)


# with db.session.begin():
#     db.session.add_all([u1, u2, u3])


# def create_data(app, db):
#     with app.app_context():
#         db.create_all()
#
#         u1 = User(username="vasya", password="my_little_pony", role="user")
#         u2 = User(username="oleg", password="qwerty", role="user")
#         u3 = User(username="oleg", password="P@ssw0rd", role="admin")
#
#         with db.session.begin():
#             db.session.add_all([u1, u2, u3])

exit()

# TO bullit work

