from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from resources.user_resource import SignUp, SignIn, SignOut
from resources.package_resource import Packages, Package
from resources.tracking_resource import Trackings, Tracking
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DoNotTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def createDatabase():
    database.create_all()


@jwt.token_in_blocklist_loader
def BlacklistVerification(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def InvalidAccessToken(self, token):
    return jsonify({'message': 'You have been logged out'}), 401


api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')
api.add_resource(SignOut, '/signout')

api.add_resource(Packages, '/packages/<string:user_id>')
api.add_resource(Package, '/package/<string:package_code>')

api.add_resource(Trackings, '/trackings')
api.add_resource(Tracking, '/tracking/<int:tracking_id>')

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)
