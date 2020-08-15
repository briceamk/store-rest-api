from flask_restful import Resource, reqparse
from constant import \
    HTTP_STATUS_CONFLICT, \
    HTTP_STATUS_CREATED
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True, help='username is required'
    )
    parser.add_argument(
        'password', type=str, required=True, help='password is required'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with username {} already exist'.format(data['username'])}, HTTP_STATUS_CONFLICT

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, HTTP_STATUS_CREATED
