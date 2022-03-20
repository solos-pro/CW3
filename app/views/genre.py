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
        page_num = request.args.get("page")
        all_genres = genre_service.get_all(page_num)
        return genre_schema.dump(all_genres, many=True), 200

    @admin_required
    def post(self, token_data):
        r_json = request.json
        genre_service.create(r_json)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @login_required
    def get(self, token_data, gid):
        # TODO: How to exclude an argument "token_data"?
        '''
            File "CW3/app/tools/auth.py", line 26, in wrapper
            return func(*args, **kwargs, token_data=token_data)
            TypeError: get() got an unexpected keyword argument 'token_data
        '''
        genre = genre_service.get_one(gid)
        if not genre:
            return "", 404
        return genre_schema.dump(genre)

    @admin_required
    def put(self, token_data, gid):
        reg_json = request.json
        reg_json["id"] = gid

        genre_service.get_update(reg_json)

        return "", 204

    # @admin_required
    # def patch(self, gid):
    #     reg_json = request.json
    #     reg_json["id"] = gid
    #
    #     genre_service.update_partial(reg_json)
    #
    #     return "", 204
    #
    # @admin_required
    # def delete(self, gid):
    #     genre_service.delete(gid)
    #
    #     return "", 204

