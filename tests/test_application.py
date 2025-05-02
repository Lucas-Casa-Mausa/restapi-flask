import pytest
from application import create_app
from application.db import db
from urllib.parse import quote


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        with app.app_context():
            database = db.get_db()
            for coll in database.list_collection_names():
                database.drop_collection(coll)
            yield app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "lucas",
            "last_name": "casa Mausa",
            "cpf": "809.561.830-69",
            "email": "teste1234@gmail.com",
            "birth_date": "1999-12-10T00:00:00Z"
                }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "lucas",
            "last_name": "casa Mausa",
            "cpf": "809.561.830-68",
            "email": "teste1234@gmail.com",
            "birth_date": "1999-12-10T00:00:00Z"
                }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 201
        assert b"successfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        post_resp = client.post('/user', json=valid_user)
        assert post_resp.status_code == 201

        encoded_cpf = quote(valid_user["cpf"])
        response = client.get(f'/user/{encoded_cpf}')
        assert response.status_code == 200

        user_data = response.json[0]
        assert user_data["first_name"] == "lucas"
        assert user_data["last_name"] == "casa Mausa"
        assert user_data["cpf"] == "809.561.830-69"
        assert user_data["email"] == "teste1234@gmail.com"
        assert user_data["birth_date"] == "1999-12-10T00:00:00Z"

        encoded_invalid_cpf = quote(invalid_user["cpf"])
        response = client.get(f'/user/{encoded_invalid_cpf}')
        assert response.status_code == 404
