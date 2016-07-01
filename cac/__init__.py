"""
cac - a client for the cloudatcost.com API
"""
__author__ = 'Sean Summers'
__version__ = '0.0.1-dev'
__license__ = 'GPL-3.0+'


from operator import itemgetter


BASE_URL = 'https://panel.cloudatcost.com/api'
API_VERSION = 'v1'


HTTP_ERRORS = {
    400: "Invalid api URL",
    403: "Invalid or missing api key",
    412: "Request failed",
    500: "Internal server error",
    503: "Rate limit hit",
}


API_RESPONSE_GETTER = {
    'ok': itemgetter('data'),
    'error': itemgetter('error', 'error_description'),
}
TEMPLATE_GETTER = itemgetter('ce_id', 'name')


from .cac import CAC
__all__ = ['CAC']
