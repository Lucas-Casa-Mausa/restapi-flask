from .db import db


class UserModel(db.Document):
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    cpf = db.StringField(required=True, unique=True)
    birth_date = db.DateTimeField(required=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "cpf": self.cpf,
            "email": self.email,
            "birth_date": self.birth_date.isoformat() + "Z"  # Formato ISO
        }


class HealthCheckModel(db.Document):
    status = db.StringField(required=True)
