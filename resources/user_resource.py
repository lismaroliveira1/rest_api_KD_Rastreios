from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt


arguments = reqparse.RequestParser()
arguments.add_argument('username', type=str, required=True)
arguments.add_argument('email', type=str, required=True)
arguments.add_argument('password', type=str, required=True)


class SignUp(Resource):
    def post(self):
        userData = arguments.parse_args()
        if UserModel.findByEmail(userData['email']):
            return {"message": "The user {} already exists".format(userData['email'])}
        newUser = UserModel(**userData)
        newUser.createUser()
        access_token = create_access_token(identity=newUser.user_id)
        return {"message": "User '{}' created successfully".format(newUser.login),
                "access_token": access_token,
                "uid": newUser.user_id,
                "createdAt": timeNow}, 201
