import requests


def push_notification(
    notification: dict,
    data: dict,
    firebase_token: str,
    server_key: str
) -> requests.Response:
    """
    :param notification: {
      "title": "firebase",
      "body": "firebase is awesome",
      "click_action": "http://localhost:3000/",
      "icon": "http://localhost:3000/assets/images/brand-logo.png"
    }
    :param data: {}
    :param firebase_token:
    :param server_key:
    :return:
    """
    url = 'https://fcm.googleapis.com/fcm/send'
    response = requests.post(
        url=url,
        json={
            'notification': notification,
            'data': data,
            'to': firebase_token
        },
        headers={
            'Authorization': f'key={server_key}'
        }
    )
    return response
