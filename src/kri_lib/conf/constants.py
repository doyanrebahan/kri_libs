from enum import Enum


class ServiceConnection(Enum):
    """
    Define which service should be connected.
    """

    SSO = 'SSO'
    COMMERCE = 'COMMERCE'
    PAYMENT = 'PAYMENT'
    WALLET = 'WALLET'
