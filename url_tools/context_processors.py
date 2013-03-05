from __future__ import unicode_literals

import urlparse

from django.http.request import QueryDict
from django.utils.encoding import iri_to_uri


class UrlHelper(object):
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
        for key in kwargs:
            val = kwargs[key]
            if hasattr(val, '__iter__'):
                self.query_dict.setlist(key, [iri_to_uri(v) for v in val])
            else:
                self.query_dict[key] = iri_to_uri(val)
