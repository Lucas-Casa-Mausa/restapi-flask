from flask import Flask
from flask_restful import Resource,Api

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        return {"message":"User 1"}

class User(Resource):
    def get(self):
        return {"message":"teste"}
    

    

api.add_resource(Users,'/users')
api.add_resource(User,'/user','/user/<string:cpf>')

if __name__ == '__main__':
    app.run(host="127.0.0.1",port="8000",debug=True)

