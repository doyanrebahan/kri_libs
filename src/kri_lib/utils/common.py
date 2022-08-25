import random
import string
from requests.models import PreparedRequest


def random_string(size=6):
    """
    generate random string for tokenizer
    """
    chars = (string.ascii_uppercase
             + string.ascii_lowercase
             + string.digits)
    return ''.join(random.choice(chars) for _ in range(size))


def add_query_params(url: str, params: dict) -> str:

    request = PreparedRequest()
    request.prepare_url(url, params)
    return request.url
