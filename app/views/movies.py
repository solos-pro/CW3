from flask import request
from flask_restx import Resource, Namespace
from app.model.movie import MovieSchema, MovieSchemaSearch
from app.container import movie_service
from app.tools.auth import admin_required, login_required

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movie_schema_search = MovieSchemaSearch()


@movie_ns.route('/')
class MoviesView(Resource):
    @login_required
    def get(self, token_data):
        search_request = {"director_id": request.args.get('director_id'),
                          "genre_id": request.args.get('genre_id'),
                          "status": request.args.get("status"),
                          "page": request.args.get("page")
                          }
        result = movie_service.search(search_request)
        return movie_schema_search.dump(result, many=True), 200

    @admin_required
    def post(self, token_data):
        r_json = request.json
        movie_service.create(r_json)
        return "", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @login_required
    def get(self, token_data, mid):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie, many=False)

    @admin_required
    def put(self, token_data, mid):
        reg_json = request.json
        reg_json["id"] = mid
        movie_service.update(reg_json)
        return "", 204

    @admin_required
    def patch(self, token_data, mid):
        reg_json = request.json
        reg_json["id"] = mid
        movie_service.update_partial(reg_json)
        return "", 204

    @admin_required
    def delete(self, token_data, mid: int):
        movie_service.delete(mid)
        return "", 204
