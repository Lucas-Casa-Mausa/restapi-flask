from flask import Flask,jsonify
from flask_restful import Resource,Api
from flask_mongoengine import MongoEngine
# from mongoengine import Document,StringField


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db':'users',
    'host':'mongodb',
    'port':'27017',
    'username':'admin',
    'password':'admin',
}


api = Api(app)
db =  MongoEngine(app)


class UserModel(db.Document):
    email = db.EmailField(required = True)
    first_name = db.StringField(required = True)
    last_name = db.StringField(required = True)
    cpf = db.StringField(required = True, unique = True)
    birthday = db.DateTimeField(required = True)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())
        # return {"message":"User 1"}

class User(Resource):
    def get(self):
        return {"message":"CPF"}
    

api.add_resource(Users,'/users')
api.add_resource(User,'/user','/user/<string:cpf>')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

