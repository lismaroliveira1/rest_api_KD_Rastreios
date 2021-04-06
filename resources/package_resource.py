from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.package_model import PackageModel


class Packages(Resource):
    @jwt_required()
    def get(self):
        return {"packages": [package.toJson for package in PackageModel.query.all()]}, 200


class Package(Resource):
    argument = reqparse.RequestParser()
    argument.add_argument('user_id', type=str, required=True)
    argument.add_argument('name', type=str, required=True)

    def get(self, package_code):
        package = PackageModel.findPackage(package_code)
        if package:
            return package.toJson()
        return {"message": "Package not found"}

    def post(self, packageCode):
        if PackageModel.findPackage(packageCode):
            return {"message": "Package '{}' already exists".format(packageCode)}
        packageData = Package.argument.parse_args()
        newPackage = PackageModel(packageCode, **)
        newPackage.savePackage()
        return newPackage.toJson()

    def put(self):
        pass

    def delete(self):
        pass
