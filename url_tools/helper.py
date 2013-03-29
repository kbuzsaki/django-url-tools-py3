from __future__ import absolute_import, unicode_literals

import urllib
import urlparse
import hashlib

from django.http.request import QueryDict
from django.utils.encoding import iri_to_uri


class UrlHelper(object):
    _hash = None

    def __init__(self, full_path):
        # parse the path
        r = urlparse.urlparse(full_path)
        self.path = r.path
        self.fragment = r.fragment
        self.query_dict = QueryDict(r.query, mutable=True)

    def get_query_string(self, **kwargs):
        return self.query_dict.urlencode(**kwargs)

    def get_query_data(self):
        return self.query_dict

    def update_query_data(self, **kwargs):
        self._hash = None
        for key in kwargs:
            val = kwargs[key]
            if hasattr(val, '__iter__'):
                self.query_dict.setlist(key, [iri_to_uri(v) for v in val])
            else:
                self.query_dict[key] = iri_to_uri(val)

    def get_path(self):
        return self.path

    def get_full_path(self, **kwargs):
        query_string = self.get_query_string(**kwargs)
        if query_string:
            query_string = '?%s' % query_string
        fragment = self.fragment and '#%s' % iri_to_uri(self.fragment) or ''

        return '%s%s%s' % (
            iri_to_uri(self.get_path()),
            query_string,
            fragment
        )

    def get_full_quoted_path(self, **kwargs):
        return urllib.quote_plus(self.get_full_path(**kwargs), safe='/')

    def del_param(self, param):
        try:
            del self.query_dict[param]
        except KeyError:
            pass # Fail silently

    def del_params(self, *params):
        if not params:
            self.query = {}
            return
        for param in params:
            self.del_param(param)

    @property
    def hash(self):
        if self._hash:
            return self._hash
        md5 = hashlib.md5()
        md5.update(self.get_full_path())
        self._hash = md5.hexdigest()
        return self._hash

    @property
    def query(self):
        return self.get_query_data()

    @query.setter
    def query(self, value):
        self._hash = None
        if type(value) is dict:
            self.query_dict = QueryDict('', mutable=True)
            self.update_query_data(**value)
        else:
            self.query_dict = QueryDict(value, mutable=True)

    @property
    def query_string(self):
        return self.get_query_string()

    @query_string.setter
    def query_string(self, value):
        self._hash = None
        self.query_dict = QueryDict(value, mutable=True)

    def __str__(self):
        return self.get_full_path()
