from marshmallow import Schema, fields
from app.database import db


# class Group(db.Model):
#     __tablename__ = 'group'
#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String, unique=True)


# class Favorite(db.Model):
#     __tablename__ = 'favorite'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre_id = db.Column(db.String, db.ForeignKey("genre.id"))
    favorite_genre = db.relationship("Genre")


    # role_id = db.Column(db.String, db.ForeignKey("group.id"))
    # role = db.relationship("Group")


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    password = fields.Str(load_only=True)
    favorite_genre = fields.Str()

    # role = fields.Str()


# class GroupSchema(Schema):
#     id = fields.Int()
#     role = fields.Str()
