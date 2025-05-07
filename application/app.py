from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from datetime import datetime
import re
from .model import UserModel
from dateutil import parser as date_parser


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


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):

    def validate_cpf(self, cpf):
        # Verifica a formatação (opcional, dependendo do uso)
        if not re.match(r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$', cpf):
            return False

        # Extrai apenas os dígitos
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica tamanho e sequências inválidas
        if len(numbers) != 11 or numbers == numbers[::-1]:
            return False

        # Validação do primeiro dígito verificador
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9],
                                                    range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10],
                                                    range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message": "CPF is invalid"}, 400

        try:
            data["birth_date"] = (
                datetime.fromisoformat(
                    data["birth_date"].replace('Z', '')
                )
            )

            user = UserModel(**data).save()
            return {
                "message": f"User {user.id} successfully created!",
                "id": str(user.id)
            }, 201

        except NotUniqueError:
            return {"message": "CPF already exists in database"}, 400
        except ValueError as e:
            return {"message": f"Invalid date format: {str(e)}"}, 400

    def get(self, cpf):
        users = UserModel.objects(cpf=cpf)
        if not users:
            return {"message": "Usuário não encontrado"}, 404

        return jsonify([user.to_dict() for user in users])

    def patch(self):
        data = _user_parser.parse_args()
        cpf = data["cpf"]

        response = UserModel.objects(cpf=cpf)
        if not response:
            return {"message": "User does not exists in database"}, 404

        if not self.validate_cpf(cpf):
            return {"message": "CPF is invalid"}, 400

        update_data = {
            k: v for k, v in data.items()
            if k != "cpf" and v is not None
        }

        if "birth_date" in update_data:
            try:
                update_data["birth_date"] = date_parser.isoparse(
                    update_data["birth_date"]
                )
            except (ValueError, TypeError):
                return {"message": "Invalid birth_date format"}, 400

        if not update_data:
            return {"message": "No valid fields to update"}, 400

        set_kwargs = {
            f"set__{k}": v for k, v in update_data.items()
        }
        response.update(**set_kwargs)

        return {"message": "User updated"}, 200

    def delete(self, cpf):
        response = UserModel.objects(cpf=cpf)

        if response:
            response.delete()
            return {"message": "User deleted"}, 200
        else:
            return {"message": "User does not exists in database"}, 404
