import requests


def push_notification(
    payload: dict,
    firebase_token: str,
    server_key: str
) -> requests.Response:
    """
    :param payload: {
      "title": "firebase",
      "body": "firebase is awesome",
      "click_action": "http://localhost:3000/",
      "icon": "http://localhost:3000/assets/images/brand-logo.png"
    }
    :param firebase_token:
    :param server_key:
    :return:
    """
    url = 'https://fcm.googleapis.com/fcm/send'
    response = requests.post(
        url=url,
        json={
            'notification': payload,
            'to': firebase_token
        },
        headers={
            'Authorization': f'key={server_key}'
        }
    )
    return response
