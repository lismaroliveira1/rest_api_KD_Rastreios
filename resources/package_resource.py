from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.package_model import PackageModel


class Packages(Resource):
    @jwt_required()
    def get(self):
        return {"packages": [package.toJson for package in PackageModel.query.all()]}, 200
