from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.package_model import PackageModel


class Packages(Resource):
    def get(self, 'user_id'):
        return {"packages": [package.toJson() for package in PackageModel.query.filter_by(user_id=user_id)all()]}, 200


class Package(Resource):
    argument = reqparse.RequestParser()
    argument.add_argument('name', type=str, required=True)
    argument.add_argument('user_id', type=str, required=True)

    def get(self, package_code):
        package = PackageModel.findPackage(package_code)
        if package:
            return package.toJson(), 200
        return {"message": "Package not found"}, 400

    def post(self, package_code):
        if PackageModel.findPackage(package_code):
            return {"message": "Package '{}' already exists".format(package_code)}, 409
        packageData = Package.argument.parse_args()
        newPackage = PackageModel(package_code, **packageData)
        try:
            newPackage.savePackage()
        except:
            return{'message': "Internal server error"}, 500
        return newPackage.toJson(), 200

    def put(self, package_code):
        package = PackageModel.findPackage(package_code)
        package_data = Package.argument.parse_args()
        if package:
            package.updatePackage(package_code, **package_data)
            try:
                package.savePackage()
                return package.toJson(), 200
            except:
                return {'message': "Internal server error"}, 500
        new_package = PackageModel(package_code, **package_data)
        try:
            new_package.savePackage()
            return new_package.toJson(), 201
        except:
            return {"message": "Internal server error"}

    def delete(self, package_code):
        package = PackageModel.findPackage(package_code)
        if package:
            try:
                package.deletePackage()
            except:
                return{'message': "Internal server error"}, 500
            return {"message": "Package deleted successfully"}, 200
        return {"message": "Package not found"}, 400
