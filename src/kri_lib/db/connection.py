from pymongo import MongoClient

from kri_lib.conf.settings import settings

"""
TODO: Implement class Connection with magic method slicing.
connection = Connection()
connection['log']
"""


class Connections:
    """
    Lazy db connections.
    """

    def __init__(self):
        self._db_conn_mapping = {
            'default': settings.DATABASES.get('default'),
            'log': settings.LOGGING.get('DATABASE')
        }
        self.db_connections = {}

    def __getitem__(self, item):

        if isinstance(item, slice):
            raise AttributeError('cannot slice db connections.')
        if item not in self._db_conn_mapping:
            raise ValueError(f'{item} is not valid connection.')

        if item not in self.db_connections:
            self.db_connections[item] = MongoClient(
                self._db_conn_mapping[item],
                uuidRepresentation='standard'
            ).get_database()
        return self.db_connections[item]


connection = Connections()
