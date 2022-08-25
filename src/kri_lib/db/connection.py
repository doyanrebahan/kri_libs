try:
    """
    NOTE: not all services need db connection.
    so we didn't include pymongo in package requirements.
    """
    from pymongo import MongoClient
except ImportError:
    raise ImportError("pymongo is required for using db connection.")

from kri_lib.conf.settings import settings


mongo_connection = MongoClient(settings.DATABASES.get('default'), uuidRepresentation='standard')

database = mongo_connection.get_database()
