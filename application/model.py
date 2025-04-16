from .db import db


class UserModel(db.Document):
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    cpf = db.StringField(required=True, unique=True)
    birthday = db.DateTimeField(required=True)
