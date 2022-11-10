from datetime import datetime
from traceback import TracebackException

import requests
from kri_lib.conf import settings
from kri_lib.core.globals import GLOBALS
from .utils import get_traceback_info, get_git_branch, get_git_blame_email, to_diff_for_human
from .document import Responsible


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
    member = Responsible().find_one({
        'github_email': email
    })
    service_name = settings.LOGGING.get('SERVICE_NAME')
    if member:
        responsible = f"<@{member.get('slack_id')}>"
    else:
        responsible = email

    slack_url = settings.LOGGING.get('SLACK').get('HOOKS_URL')
    blocks = [
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
                    "text": f"*Datetime:*\n{to_diff_for_human(datetime.now())}"
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
        }
    ]
    response = requests.post(slack_url, json={
        "text": repr(exception),
        "blocks": blocks
    })
    if not response.ok:
        if response.text == 'invalid_blocks':
            message = ":ghost: *Couldn't display errors traceback, message contains restricted" \
                      " chars, please check manually on your database based on `API_ID`*"
            blocks[-1].get('text').update({'text': message})
            response = requests.post(slack_url, json={
                "text": repr(exception),
                "blocks": blocks
            })
        print(response.text)
