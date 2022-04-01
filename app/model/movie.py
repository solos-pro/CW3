from marshmallow import Schema, fields
from app.database import db
from app.model.genre import GenreSchema
from app.model.director import DirectorSchema

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
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    name = fields.Str(required=True)
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)
    description = fields.Str(required=True)
    trailer = fields.Str(required=True)
    year = fields.Int(required=True)
    rating = fields.Float(required=True)


class MovieSchemaSearch(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    year = fields.Int(required=True)
    rating = fields.Float(required=True)
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)

