import mysql.connector
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
            config = self._db_conn_mapping[item]
            self.db_connections[item] = mysql.connector.connect(
                host=config['HOST'],
                user=config['USER'],
                password=config['PASSWORD'],
                database=config['NAME'],
                port=config.get('PORT', 3306)
            )
        return self.db_connections[item]


connection = Connections()
