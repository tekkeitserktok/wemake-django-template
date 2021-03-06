# -*- coding: utf-8 -*-

import re
import sys

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


MODULE_REGEX = r'^[a-z][_a-z0-9]+$'
MODULE_NAME = '{{ cookiecutter.project_name }}'

DOMAIN_NAME = '{{ cookiecutter.project_domain }}'


def validate_project_name():
    """
    This validator is used to ensure that `project_name` is valid.

    Valid inputs starts with the lowercase letter.
    Followed by any lowercase letters, numbers or underscores.

    Valid example: `school_project3`.
    """
    if not re.match(MODULE_REGEX, MODULE_NAME):
        # Validates project's module name:
        message = (
            'ERROR: The project slug {} is not a valid Python module name. '
            'Start with a lowercase letter. '
            'Followed by any lowercase letters, numbers or underscores.'
        )
        raise ValueError(message.format(MODULE_NAME))


def validate_domain():
    """
    This validator is used to enforce correct `project_domain` inputs.

    What is considered valid:
    1. myapp.com
    2. google.co.uk

    What is considered invalid:
    1. https://wemake.services
    2. http://mysite.ru/hello
    3. http://myshop.com?query=django
    """
    result = urlparse(DOMAIN_NAME)
    if not result.path:
        # When entering just a domain everything inside goes to `path`.
        # So, it should be set. If not, that's an error.
        raise ValueError(
            'ERROR: `project_domain` is invalid. '
            'Try to drop the `http(s)://` part.',
        )

    parts = [
        result.scheme,
        result.netloc,
        result.params,
        result.query,
        result.fragment,
    ]
    if any(bool(part) for part in parts):
        raise ValueError(
            'ERROR: `project_domain` should be a domain name only. '
            'Without params, query or any other url parts.',
        )


try:
    validate_project_name()
    validate_domain()
except ValueError as e:
    print(e)
    sys.exit(1)
