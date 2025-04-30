import os


class DevConfig():

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USER'),
        'password': os.getenv('MONGODB_PASSWORD'),
    }


class ProdConfig():

    MONGODB_USER = os.getenv('MONGODB_USER')
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
    MONGODB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_DB = os.getenv("MONGODB_DB")

    MONGODB_SETTINGS = {
        'host': f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}'
        f'@{MONGODB_HOST}?retryWrites=true&w=majority&appName={MONGODB_DB}'
    }


class MockConfig():

    MONGODB_SETTINGS = {
        'db': "users",
        'host': "mongomock://localhost",
    }
