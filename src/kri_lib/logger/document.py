from kri_lib.db.connection import connection
from kri_lib.utils.common import pascal_to_snake_case


class BaseDocument:

    @property
    def fields(self):
        raise NotImplementedError('fields must be overridden.')

    @property
    def collection_name(self):
        return pascal_to_snake_case(self.__class__.__name__)

    def get_payload_save(self):
        payload = {}
        for field in self.fields:
            payload[field] = getattr(self, field)
        return payload

    def connection(self):
        return connection['log'][self.collection_name]

    def find_one(self, search):
        return (self.connection().find_one(search))

    def save(self):
        return (self.connection().insert_one(self.get_payload_save()))


class BaseLogRequest(BaseDocument):
    service_name: str
    url: str
    method: str
    headers: str
    payload: str
    api_id: str
    response_status: int

    @property
    def fields(self):
        return [
            'service_name',
            'url',
            'method',
            'headers',
            'payload',
            'api_id',
            'response_status'
        ]


class LogRequest(BaseLogRequest):
    pass


class LogError(BaseDocument):
    """
    TODO: Add stack trace errors.
    """
    service_name: str
    url: str
    method: str
    headers: dict
    payload: str
    api_id: str
    stack_traces: list

    @property
    def fields(self):
        return [
            'service_name',
            'url',
            'method',
            'headers',
            'payload',
            'api_id',
            'stack_traces'
        ]


class Responsible(BaseDocument):
    """
    Keep github email and slack's member_id who has responsibility
    """
    github_email: str
    slack_id: str

    @property
    def fields(self):
        return [
            'github_email',
            'slack_id'
        ]
