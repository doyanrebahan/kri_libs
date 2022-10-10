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

    def save(self):
        return (connection['log'][self.collection_name]
                .insert_one(self.get_payload_save()))


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
