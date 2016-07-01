try:
    from six import iteritems
except ImportError:
    iteritems = dict.iteritems

from . import TEMPLATE_GETTER
from .util import argv_checker
from .util import make_url
from .util import web_request


class CAC(object):

    def __init__(self, email, api_key):
        self.credentials = {
            'login': email,
            'key': api_key
        }

    def _response(self, url, data=None, verify=False):
        params = self.credentials.copy()
        if not data:
            response = web_request(url, params=params)
        else:
            data.pop('self', None)
            params.update(data)
            response = web_request(url, data=params)
        data = locals()
        return response

    @property
    def servers(self):
        url = make_url('listservers')
        response = {__.pop('id'): __ for __ in self._response(url)}
        assert all(k == v['sid'] for k, v in iteritems(response))
        return response

    @property
    def templates(self):
        url = make_url('listtemplates')
        response = dict(TEMPLATE_GETTER(__) for __ in self._response(url))
        return response

    @property
    def tasks(self):
        url = make_url('listtasks')
        response = self._response(url)
        return response

    @property
    def resources(self):
        url = make_url('cloudpro/resources')
        response = self._response(url)
        return response

    def _check_sid(self, sid):
        assert sid in self.servers.keys(), \
            "sid={}: server not found".format(sid)

    def console(self, sid=None):
        self._check_sid(sid)

        data = locals()
        url = make_url('console')

        response = self._response(url, data)
        return response

    def delete(self, sid=None):
        self._check_sid(sid)

        data = locals()
        url = make_url('cloudpro/delete')

        response = self._response(url, data)
        return response

    def renameserver(self, sid=None, name=None):
        self._check_sid(sid)

        data = locals()
        url = make_url('renameserver')

        response = self._response(url, data)
        return response

    def rdns(self, sid=None, hostname=None):
        self._check_sid(sid)

        data = locals()
        url = make_url('rdns')

        response = self._response(url, data)
        return response

    @argv_checker(mode={'normal', 'safe'})
    def runmode(self, sid=None, mode=None):
        self._check_sid(sid)

        data = locals()
        url = make_url('runmode')

        response = self._response(url, data)
        return response

    @argv_checker(action={'poweron', 'poweroff', 'reset'})
    def powerop(self, sid=None, action=None):
        self._check_sid(sid)

        data = locals()
        url = make_url('powerop')

        response = self._response(url, data)
        return response

    @argv_checker(
        ram={str(__) for __ in range(512, 32769, 4)},
        storage={str(__) for __ in range(10, 1001, 5)},
        cpu={str(__) for __ in range(1, 17)},
    )
    def build(self, os='26', ram='512', storage='10', cpu='1'):
        assert os in self.templates.keys(), \
            "os={}: os image not found".format(os)

        data = locals()
        url = make_url('cloudpro/build')

        response = self._response(url, data)
        return response
