from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb',
    'port': '27017',
    'username': 'admin',
    'password': 'admin',
}


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help='This Field cannot be blank'
                          )
_user_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help='This Field cannot be blank'
                          )
_user_parser.add_argument('cpf',
                          type=str,
                          required=True,
                          help='This Field cannot be blank'
                          )
_user_parser.add_argument('birth_date',
                          type=str,
                          required=True,
                          help='This Field cannot be blank'
                          )
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help='This Field cannot be blank'
                          )

api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    cpf = db.StringField(required=True, unique=True)
    birthday = db.DateTimeField(required=True)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())



class User(Resource):
    def post(self):
        data = _user_parser.parse_args()
        UserModel(**data).save()


    def get(self):
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
