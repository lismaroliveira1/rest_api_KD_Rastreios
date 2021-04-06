from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.package_model import PackageModel


class Packages(Resource):
    @jwt_required()
    def get(self):
        return {"packages": [package.toJson() for package in PackageModel.query.all()]}


class Package(Resource):
    argument = reqparse.RequestParser()
    argument.add_argument('name', type=str, required=True)
    argument.add_argument('user_id', type=str, required=True)

    def get(self, package_code):
        package = PackageModel.findPackage(package_code)
        if package:
            return package.toJson()
        return {"message": "Package not found"}

    def post(self, package_code):
        if PackageModel.findPackage(package_code):
            return {"message": "Package '{}' already exists".format(package_code)}
        packageData = Package.argument.parse_args()
        newPackage = PackageModel(package_code, **packageData)
        newPackage.savePackage()
        return newPackage.toJson(), 200

    def put(self, package_code):
        package_data = Package.argument.parse_args()
        package = PackageModel.findPackage(package_code)
        if package:
            package.updatePackage(package_code, **package_data)
            package.savePackage()
            return {"message": "Package updated successfully"}
        return {"message": "Package not found"}
