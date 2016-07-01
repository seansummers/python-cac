import functools
import inspect

import requests

try:
    from six import iteritems
    from six.moves import zip
except ImportError:
    iteritems = dict.iteritems

from . import API_RESPONSE_GETTER
from . import API_VERSION
from . import BASE_URL
from . import HTTP_ERRORS


def argv(f):
    args, _, _, defaults = inspect.getargspec(f)
    return dict(zip(reversed(args), reversed(defaults)))


def response_parser(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        http_status = response.status_code
        error = HTTP_ERRORS.get(http_status, None)
        if error:
            raise Exception("API error {}: {}".format(http_status, error))
        try:
            response = response.json()
            status = response['status']
            getter = API_RESPONSE_GETTER[status]
            response = getter(response)
        except ValueError:
            response = response.text
        except KeyError:
            pass
        return response
    return wrapper


def argv_checker(f=None, **tests):
    if not f:
        return functools.partial(argv_checker, **tests)

    default_kwargs = argv(f)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        _kwargs = default_kwargs.copy()
        _kwargs.update(kwargs)
        for arg, test in iteritems(tests):
            if _kwargs[arg] not in test:
                raise ValueError(
                    "{}={}: must be one of {}".format(
                        arg, _kwargs[arg], test
                    )
                )
        return f(*args, **_kwargs)
    return wrapper


def make_url(command):
    return '/'.join((BASE_URL, API_VERSION, '{}.php'.format(command)))


@response_parser
def web_request(url, params=None, data=None, verify=False):
    if params:
        response = requests.get(url, verify=verify, params=params)
    if data:
        response = requests.post(url, verify=verify, data=data)
    return response
