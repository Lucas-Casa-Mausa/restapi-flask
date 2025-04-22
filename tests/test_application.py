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
            "email": "teste1234@gmailcom.",
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