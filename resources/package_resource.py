from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.package_model import PackageModel


class Packages(Resource):
    def get(self):
        return {"packages": [package.toJson() for package in PackageModel.query.all()]}, 200


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
        package_data = Package.arguments.parse_args()
        package = PackageModel.findPackage(package_code)
        if package:
            package.updatePackage(package_code, **package_data)
            try:
                newPackage.savePackage()
            except:
                return{'message': "Internal server error"}, 500
            return {"message": "Package updated successfully"}, 200
        return {"message": "Package not found"}, 400

    def delete(self, package_code):
        package = PackageModel.findPackage(package_code)
        if package:
            try:
                newPackage.deletePackage()
            except:
                return{'message': "Internal server error"}, 500
            return {"message": "Package deleted successfully"}, 200
        return {"message": "Package not found"}, 400
