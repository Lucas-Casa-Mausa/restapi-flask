import pytest
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "lucas",
            "last_name": "casa Mausa",
            "cpf": "403.707.058-82",
            "email": "teste1234@gmailcom.",
            "birth_date": "1999-12-10"
                }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "lucas",
            "last_name": "casa Mausa",
            "cpf": "403.707.058-81",
            "email": "teste1234@gmail.com",
            "birth_date": "1999-12-10"
                }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"sucessfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get('/user/%s' % valid_user["cpf"])
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "lucas"
        assert response.json[0]["last_name"] == "casa Mausa"
        assert response.json[0]["cpf"] == "403.707.058-82"
        assert response.json[0]["email"] == "teste1234@gmail.com"
        birth_date = response.json[0]["birth_date"]["$date"] == "1999-12-10"
        assert birth_date == "1999-12-10"

        response = client.get('/user/%s' % invalid_user["cpf"])
        assert response.status_code == 400
        assert b"User does not exist in database" in response.data
