import re
import time
from datetime import datetime
from pathlib import Path
from subprocess import check_output
from traceback import TracebackException
from urllib.parse import urljoin
from typing import Dict

import requests
from django.conf import settings as django_settings
from kri_lib.conf import settings
from kri_lib.core.globals import GLOBALS
from kri_lib.db.connection import connection


def generate_api_id():
    sequence = 'API_ID_{unique_id}'
    unique_id = datetime.now().timestamp()
    return sequence.format(
        unique_id=unique_id
    )


def get_request_body(request):
    try:
        body = getattr(request, request.method)
    except AttributeError:
        # TODO: handle this shit things:
        #  request.PUT, request.PATCH doesn't exist in request.method
        return {}
    return body


def to_preserve(payload, safe_keys):
    for key in safe_keys:
        if key in payload.keys():
            payload[key] = '*' * 5
    return payload


def db_print(*values):
    query = {
        'service_name': settings.LOGGING.get('SERVICE_NAME'),
        'api_id': GLOBALS.API_ID,
        'results': list(values)
    }
    # connection['log'].log_print.insert_one(query)
    url = urljoin(
        settings.LOGGING.get('API').get('host'),
        '/api/v1/log/log-print'
    )
    return requests.post(
        url=url,
        json=query,
        headers={
            'Authorization': settings.LOGGING.get('API').get('Authorization')
        }
    )


def log_print(*values):
    query = {
        'service_name': settings.LOGGING.get('SERVICE_NAME'),
        'api_id': GLOBALS.API_ID,
        'results': list(values)
    }
    url = urljoin(
        settings.LOGGING.get('API').get('host'),
        '/api/v1/log/log-print'
    )
    return requests.post(
        url=url,
        json=query,
        headers={
            'Authorization': settings.LOGGING.get('API').get('Authorization')
        }
    )


def get_last_traceback(tb: TracebackException):
    result = tb
    while result.tb_next:
        result = result.tb_next
    return result


def get_traceback_info(tb: TracebackException) -> Dict[str, str]:
    last_tb = get_last_traceback(tb)
    return {
        "file": last_tb.tb_frame.f_code.co_filename,
        "line_number": last_tb.tb_lineno
    }


def get_git_branch() -> str:
    proc = check_output(["git", "branch"])

    if isinstance(proc, bytes):
        proc = proc.decode('utf-8')

    branch_list = proc.strip()
    if '\n' in proc:
        branch_list = branch_list.split('\n')

    if not isinstance(branch_list, list):
        branch_list = [branch_list]

    cur_branch = None
    for branch in branch_list:
        if re.match(r'[*]', branch):
            cur_branch = branch
            break

    if cur_branch:
        cur_branch = cur_branch.replace('*', '').strip()
    return cur_branch


def get_git_blame_email(file_path: str, line_number: str):
    root = Path(django_settings.BASE_DIR)
    child = Path(file_path)
    if root in child.parents:
        commands = [
            'git',
            'blame',
            '--show-email',
            f'-L{line_number},{line_number}',
            '--',
            file_path
        ]
        proc = check_output(commands).decode()
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', proc)
        if match:
            return match.group(0)
    return "Unknown"


def to_diff_for_human(date_time: datetime) -> str:
    return date_time.strftime(f'%a %d %b %Y %H:%M:%S {time.localtime().tm_zone}')


def get_git_summary():
    commands = [
        'git', 'show', '--summary'
    ]
    proc = check_output(commands).decode()
    return proc
