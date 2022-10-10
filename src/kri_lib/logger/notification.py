from datetime import datetime
from traceback import TracebackException

import requests
from kri_lib.conf import settings
from kri_lib.core.globals import GLOBALS
from .utils import get_traceback_info, get_git_branch, get_git_blame_email

"""
NOTE: github email can be multiple, just add the same slack's member_id
mapping between github email and slack member_id
"""
SLACK_USERS_MAPPING = {
    'rimba47prayoga@gmail.com': 'U03M580TMFA',
    'm.rafly@kuncicoin.com': 'U03UH7ZMN7J',
    'erhanburhanudin@gmail.com': 'U030P1P4DL6',
    'a.fransisko@kuncicoin.com': 'U03L11LL5TJ',
    'sdimasfarhan@gmail.com': 'U0318ADM0UR'
}


def notify_to_slack(
    exception: Exception,
    tb: TracebackException,
    stack_traces: str,
    endpoint: str
):
    tb_info = get_traceback_info(tb)
    email = get_git_blame_email(
        file_path=tb_info.get('file'),
        line_number=tb_info.get('line_number')
    )
    member_id = SLACK_USERS_MAPPING.get(email)
    service_name = settings.LOGGING.get('SERVICE_NAME')
    if member_id:
        responsible = f'<@{member_id}>'
    else:
        responsible = email

    slack_url = settings.LOGGING.get('SLACK').get('HOOKS_URL')
    payload = {
        "text": repr(exception),
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": repr(exception),
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Service:*\n{service_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Branch:*\n{get_git_branch()}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Endpoint:*\n`{endpoint}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*API ID:*\n`{GLOBALS.API_ID}`"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Responsible:*\n{responsible}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Datetime:*\n{datetime.now()}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Traceback:*\n```{stack_traces}```"
                }
            },
        ]
    }
    response = requests.post(slack_url, json=payload)
    if not response.ok:
        print(response.text)
