from flask import request
from flask_restx import Resource, Namespace
from app.tools.auth import login_required, admin_required

from app.container import director_service
from app.model.director import DirectorSchema

director_ns = Namespace('directors')
director_schema = DirectorSchema()


@director_ns.route('/')
class DirectorsView(Resource):
    @login_required
    def get(self):
        all_directors = director_service.get_all()
        return director_schema.dump(all_directors, many=True), 200

    @admin_required
    def post(self):
        r_json = request.json
        director_service.create(r_json)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @login_required
    def get(self, did):
        director = director_service.get_one(did)
        if not director:
            return "", 404
        return director_schema.dump(director)

    @admin_required
    def put(self, did):
        reg_json = request.json
        reg_json["id"] = did

        director_service.get_update(reg_json)
        return "", 204

    @admin_required
    def patch(self, did):
        reg_json = request.json
        reg_json["id"] = did

        director_service.update_partial(reg_json)

        return "", 204

    @admin_required
    def delete(self, did):
        director_service.delete(did)

        return "", 204