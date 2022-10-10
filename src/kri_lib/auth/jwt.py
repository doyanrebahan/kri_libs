import jwt
from calendar import timegm
from datetime import datetime

from kri_lib.conf.settings import settings
from kri_lib.db.connection import connection
from kri_lib.db.exceptions import UserNotFoundError
from kri_lib.db.utils import get_user_by_uuid
from kri_lib.utils import random_string


def _get_user(user_uuid: str):

    try:
        user = get_user_by_uuid(user_uuid)
    except UserNotFoundError:
        """
        already validated by kunci_account_service,
        that user is exists in mysql db.
        """
        user_secret_key = generate_jwt_secret()
        user = {
            'user_uuid': user_uuid,
            'jwt_secret': user_secret_key
        }

        connection['default'].user.insert_one(user)
    else:
        user_secret_key = user.get("jwt_secret")
        if not user_secret_key:
            user_secret_key = generate_jwt_secret()
            connection['default'].user.update_one(
                {
                    'user_uuid': user_uuid
                },
                {
                    '$set': {'jwt_secret': user_secret_key}
                }
            )
    return user


def jwt_payload_handler(payload):
    new_payload = {
        **payload,
        'exp': datetime.utcnow() + settings.JWT_AUTH.JWT_EXPIRATION_DELTA
    }

    if settings.JWT_AUTH.ALLOW_REFRESH:
        new_payload.update({
            'orig_iat': timegm(
                datetime.utcnow().utctimetuple()
            )
        })
    return new_payload


def jwt_encode_handler(user_uuid: str, payload: dict) -> str:
    user = _get_user(user_uuid)
    secret_key = f'{settings.JWT_AUTH.SECRET_KEY}||{user.get("jwt_secret")}'
    return jwt.encode(
        payload=payload,
        key=secret_key,
        algorithm=settings.JWT_AUTH.JWT_ALGORITHM
    ).decode('utf-8')


def jwt_decode_handler(jwt_value: str) -> dict:

    unverified_payload = jwt.decode(
        jwt=jwt_value,
        key=None,
        verify=False,
        algorithms=[settings.JWT_AUTH.JWT_ALGORITHM]
    )
    try:
        user = get_user_by_uuid(
            uuid=unverified_payload.get('user_uuid')
        )
    except UserNotFoundError:
        print(f"UserNotFoundError: {unverified_payload.get('user_uuid')}")
        raise jwt.InvalidTokenError("Invalid token")

    options = {
        'verify_exp': settings.JWT_AUTH.JWT_VERIFY_EXPIRATION
    }
    secret_key = f'{settings.JWT_AUTH.SECRET_KEY}||{user.get("jwt_secret")}'
    print(f'SECRET_KEY: {secret_key}')
    print(jwt_value)
    return jwt.decode(
        jwt=jwt_value,
        key=secret_key,
        options=options,
        algorithms=[settings.JWT_AUTH.JWT_ALGORITHM]
    )


def generate_jwt_secret():
    jwt_secret = random_string(50)
    is_exists = connection['default'].user.find_one({'jwt_secret': jwt_secret})
    if is_exists:
        return generate_jwt_secret()
    return jwt_secret
