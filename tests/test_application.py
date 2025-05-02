import pytest
from application import create_app
from application.db import db
from datetime import datetime, timezone


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
            "birth_date": "1999-12-10"
                }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "lucas",
            "last_name": "casa Mausa",
            "cpf": "809.561.830-68",
            "email": "teste1234@gmail.com",
            "birth_date": "1999-12-10"
                }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"successfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        post_resp = client.post('/user', json=valid_user)
        assert post_resp.status_code == 200

        response = client.get('/user/%s' % valid_user["cpf"])
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "lucas"
        assert response.json[0]["last_name"] == "casa Mausa"
        assert response.json[0]["cpf"] == "809.561.830-69"
        assert response.json[0]["email"] == "teste1234@gmail.com"

        birth_ts = response.json[0]["birth_date"]["$date"]
        birth_date = (datetime.fromtimestamp(birth_ts / 1000, tz=timezone.utc)
                      .strftime('%Y-%m-%d'))
        assert birth_date == "1999-12-10"

        response = client.get('/user/%s' % invalid_user["cpf"])
        assert response.status_code == 400
        assert b"User does not exist in database" in response.data
