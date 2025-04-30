import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


class DevConfig():

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USER'),
        'password': os.getenv('MONGODB_PASSWORD'),
    }


class ProdConfig():

    MONGODB_USERNAME = os.getenv("MONGO_USERNAME")
    MONGODB_PASSWORD = quote_plus(
        os.getenv("MONGO_PASSWORD"))
    MONGODB_CLUSTER = os.getenv("MONGO_CLUSTER")
    MONGODB_DB = os.getenv("MONGO_DB")
    MONGODB_QUERY_PARAMS = os.getenv("MONGO_QUERY_PARAMS")
    MONGODB_SETTINGS = {
        'host': f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@"
        f"{MONGODB_CLUSTER}/{MONGODB_DB}?{MONGODB_QUERY_PARAMS}"
    }


class MockConfig:
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'users',
        'host': 'mongodb://localhost',
        'mongo_client_class': 'mongomock.MongoClient',
        'alias': 'default',
        'connect': False,
        'uuidRepresentation': 'standard'
    }
