from marshmallow import Schema, fields
from app.database import db

# TODO: Why class Genre isn't imported from a genre-model?


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


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    name = fields.Str()
    genre = fields.Str()
    director = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class MovieSchemaSearch(Schema):
    id = fields.Int()
    title = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

