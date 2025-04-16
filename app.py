from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re

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

    def validate_cpf(self, cpf):

        # Has the correct mask?
        if not re.match(r'\d{3}\.\d{3}\.\d{3}\.\d{2}', cpf):
            return False

        # Grap only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Does it have 11 digits?
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validate first digit after -
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9],
                                                  range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validate second digit after -
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10],
                                                  range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message":"CPF is invalid"}

        try:
            response = UserModel(**data).save()
            return {"message":"User %s sucessfully created!" % response.id}
        except NotUniqueError:
            return {"message":"CPF already exists in database"},400

    def get(self):
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
