from flask import request
from flask_restx import Resource, Namespace

from app.container import genre_service
from app.model.genre import GenreSchema
from app.tools.auth import login_required, admin_required

genre_ns = Namespace('genres')
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresView(Resource):
    @login_required
    def get(self, token_data):
        all_genres = genre_service.get_all()
        return genre_schema.dump(all_genres, many=True), 200

    @admin_required
    def post(self):
        r_json = request.json
        genre_service.create(r_json)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @login_required
    def get(self, gid):
        genre = genre_service.get_one(gid)
        if not genre:
            return "", 404
        return genre_schema.dump(genre)

    @admin_required
    def put(self, gid):
        reg_json = request.json
        reg_json["id"] = gid

        genre_service.get_update(reg_json)

        return "", 204

    @admin_required
    def patch(self, gid):
        reg_json = request.json
        reg_json["id"] = gid

        genre_service.update_partial(reg_json)

        return "", 204

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)

        return "", 204

