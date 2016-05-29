

import urllib.request, urllib.parse, urllib.error
import urllib.parse
import hashlib

try:
    from django.http.request import QueryDict
except ImportError:  # django 1.4.2
    from django.http import QueryDict

from django.utils.encoding import iri_to_uri


def unique_list(ls):
    unique = []
    seen = set()
    for el in ls:
        if el not in seen:
            unique.append(el)
            seen.add(el)
    return unique


class OrderedQueryDict(QueryDict):

    def __init__(self, query_string=None, mutable=False, encoding=None, order=None):
        super().__init__(query_string, mutable, encoding)
        if not order:
            order = [key for key, _ in urllib.parse.parse_qsl(query_string)]
        self.order = order

    def _ordered_keys(self):
        unordered_keys = set(self.keys()).difference(self.order)
        return self.order + sorted(unordered_keys)

    def iteritems(self):
        for key in self._ordered_keys():
            yield key, self[key]

    def items(self):
        return list(self.iteritems())

    def iterlists(self):
        for key in unique_list(self._ordered_keys()):
            yield key, self.getlist(key)

    def lists(self):
        return list(self.iterlists())


class UrlHelper(object):
    def __init__(self, full_path):
        # If full_path is an UrlHelper instance, extract the full path from it
        if type(full_path) is UrlHelper:
            full_path = full_path.get_full_path()

        # parse the path
        r = urllib.parse.urlparse(full_path)
        self.path = r.path
        self.fragment = r.fragment
        self.query_dict = OrderedQueryDict(r.query, mutable=True)

    def get_query_string(self, **kwargs):
        return self.query_dict.urlencode(**kwargs)

    def get_query_data(self):
        return self.query_dict

    def update_query_data(self, **kwargs):
        for key, val in kwargs.items():
            if isinstance(val, list):
                self.query_dict.setlist(key, val)
            else:
                self.query_dict[key] = val

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
        return urllib.parse.quote_plus(self.get_full_path(**kwargs), safe='/')

    def overload_params(self, **kwargs):
        for key, val in kwargs.items():
            if val not in self.query_dict.getlist(key):
                self.query_dict.appendlist(key, val)

    def del_param(self, param):
        try:
            del self.query_dict[param]
        except KeyError:
            pass  # Fail silently

    def del_params(self, *params, **kwargs):
        if not params and not kwargs:
            self.query = {}
            return
        if params:
            for param in params:
                self.del_param(param)
        if kwargs:
            for key, val in kwargs.items():
                to_keep = [x for x in self.query_dict.getlist(key)
                           if not x.startswith(val)]
                self.query_dict.setlist(key, to_keep)

    def toggle_params(self, **params):
        for param, value in list(params.items()):
            value = str(value)
            if value in self.query_dict.getlist(param):
                self.del_params(**{param: value})
            else:
                self.overload_params(**{param: value})

    @property
    def hash(self):
        md5 = hashlib.md5()
        md5.update(self.get_full_path().encode("utf-8"))
        return md5.hexdigest()

    @property
    def query(self):
        return self.get_query_data()

    @query.setter
    def query(self, value):
        if type(value) is dict:
            self.query_dict = OrderedQueryDict('', mutable=True)
            self.update_query_data(**value)
        else:
            self.query_dict = OrderedQueryDict(value, mutable=True)

    @property
    def query_string(self):
        return self.get_query_string()

    @query_string.setter
    def query_string(self, value):
        self.query_dict = OrderedQueryDict(value, mutable=True)

    def __str__(self):
        return self.get_full_path()
