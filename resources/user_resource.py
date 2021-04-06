from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from werkzeug.security import safe_str_cmp
from models.user_model import UserModel
import random
import string
import datetime

arguments = reqparse.RequestParser()
arguments.add_argument('username', type=str, required=False)
arguments.add_argument('email', type=str, required=True)
arguments.add_argument('password', type=str, required=True)
timeNow = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


class SignUp(Resource):
    def post(self):
        userData = arguments.parse_args()
        if UserModel.findByEmail(userData['email']):
            return {"message": "The user {} already exists".format(userData['email'])}
        user_id = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=16))
        userData['user_id'] = user_id
        newUser = UserModel(** userData)
        newUser.createUser()
        access_token = create_access_token(identity=newUser.user_id)
        return {"message": "User '{}' created successfully".format(newUser.email),
                "access_token": access_token,
                "uid": newUser.user_id,
                "createdAt": timeNow}, 201


class SignIn(Resource):
    def post(self):
        userData = arguments.parse_args()
        user = UserModel.findByEmail(userData['email'])
        if user and safe_str_cmp(user.password, userData['password']):
            access_token = create_access_token(identity=user.user_id)
            return {"message": "User '{}' logged successfully".format(user.username),
                    "access_token": access_token,
                    "uid": user.user_id,
                    "loggedAt": timeNow}, 200
            return {"message": "The username or passward is incorrect"}, 401


class SignOut(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out Successfully"}, 200
