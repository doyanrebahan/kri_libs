from typing import Dict, Literal, Union
from urllib.parse import urljoin
from uuid import UUID
from kri_lib.conf import settings
from kri_lib.utils import requests


OTPTypes = Literal[
    'FORGOT_PASSWORD',
    'SEND_WALLET',
    'REGISTER',
    'REGISTER_VENDOR',
    'SWAP'
]


class OTPUtils:

    @staticmethod
    def send_otp(
        user_id: Union[str, UUID],
        email: str,
        otp_type: OTPTypes,
        notification: Dict
    ):
        """
        :param user_id:
        :param email:
        :param otp_type:
        :param notification: {
            "subject": "Send Wallet",
            "template": "otp-send-wallet",
            "extra_context": {
                "first_name": user.first_name
            }
        }
        :rtype: requests.Response
        """
        url = urljoin(
            settings.SSO_SERVICE_URL,
            '/api/v1/user/otp'
        )
        if isinstance(user_id, UUID):
            user_id = str(user_id)

        payload = {
            "user_id": user_id,
            "email": email,
            "otp_type": otp_type,
            "otp_method": "EMAIL",
            "notification": notification
        }
        return requests.post(
            url=url,
            json=payload,
            headers={
                'Authorization': settings.SSO_AUTH_HEADER
            }
        )

    @staticmethod
    def verify_otp(
        email: str,
        otp_code: str,
        otp_type: OTPTypes
    ):
        """
        :param email:
        :param otp_code:
        :param otp_type:
        :return: requests.Response
        """
        url = urljoin(
            settings.SSO_SERVICE_URL,
            '/api/v1/user/otp/verify'
        )
        payload = {
            "otp_code": otp_code,
            "email": email,
            "otp_type": otp_type,
            "otp_method": "EMAIL"
        }
        return requests.post(
            url=url,
            json=payload,
            headers={
                'Authorization': settings.SSO_AUTH_HEADER
            }
        )
