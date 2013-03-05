from __future__ import unicode_literals

from django.test import TestCase

from url_tools.context_processors import UrlHelper


class UrlHelperTestCase(TestCase):
    def test_url_helper_get_query_string(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        self.assertEqual(u.get_query_string(), 'foo=1&bar=2')

    def test_url_helper_get_query_data(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        data = u.get_query_data()
        self.assertEqual(data['foo'], '1')
        self.assertEqual(data['bar'], '2')

    def test_update_query_data(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=2)
        self.assertEqual(u.get_query_data()['foo'], '2')

    def test_update_query_data_with_multiple_values(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=[1,2,3])
        self.assertEqual(u.get_query_data()['foo'], '3')
        self.assertEqual(u.get_query_data().getlist('foo'), ['1', '2', '3'])

    def test_get_query_string_after_modification(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=2)
        self.assertEqual(u.get_query_string(), 'foo=2&bar=2')

    def test_get_query_with_multiple_values(self):
        u = UrlHelper('/foo')
        u.update_query_data(foo=[1, 2, 3])
        self.assertEqual(u.get_query_string(), 'foo=1&foo=2&foo=3')

    def test_safe_slash_argument(self):
        u = UrlHelper('/foo')
        u.update_query_data(redir='/foo/bar/')
        self.assertEqual(u.get_query_string(safe='/'), 'redir=/foo/bar/')

    def test_with_query_params_in_url(self):
        u = UrlHelper('/foo')
        u.update_query_data(redir='/foo/bar/?q=Mickey+Mouse')
        self.assertEqual(u.get_query_string(safe='/'),
                         'redir=/foo/bar/%3Fq%3DMickey%2BMouse')

    def test_get_path(self):
        u = UrlHelper('/foo')
        self.assertEqual(u.get_path(), '/foo')

    def test_get_full_path_with_no_querystring(self):
        u = UrlHelper('/foo')
        self.assertEqual(u.get_full_path(), '/foo')

    def test_get_full_path(self):
        u = UrlHelper('/foo')
        u.update_query_data(foo=1)
        self.assertEqual(u.get_full_path(), '/foo?foo=1')

    def test_retains_fragment(self):
        u = UrlHelper('/foo#bar')
        u.update_query_data(foo=1)
        self.assertEqual(u.get_full_path(), '/foo?foo=1#bar')

