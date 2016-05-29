# -*- coding: utf-8 -*-



from unittest import TestCase

from url_tools.helper import UrlHelper


class UrlHelperTestCase(TestCase):
    def test_url_helper_get_query_string(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        self.assertEqual(u.get_query_string(), 'foo=1&bar=2')

    def test_url_helper_get_query_string_unicode(self):
        u = UrlHelper('/foo?foo=1&bar=слово')
        self.assertEqual(u.get_query_string(),
                         'foo=1&bar=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE')

    def test_url_helper_get_query_data(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        data = u.get_query_data()
        self.assertEqual(data['foo'], '1')
        self.assertEqual(data['bar'], '2')

    def test_url_helper_get_query_data_unicode(self):
        u = UrlHelper('/foo?foo=1&bar=слово')
        data = u.get_query_data()
        self.assertEqual(data['foo'], '1')
        self.assertEqual(data['bar'], 'слово')

    def test_update_query_data(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=2)
        self.assertEqual(u.get_query_data()['foo'], 2)

    def test_update_query_data_unicode(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo='слово')
        self.assertEqual(u.get_query_data()['foo'], 'слово')

    def test_update_query_data_with_multiple_values(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=[1, 2, 3])
        self.assertEqual(u.get_query_data()['foo'], 3)
        self.assertEqual(u.get_query_data().getlist('foo'), [1, 2, 3])

    def test_update_query_data_with_multiple_values_unicode(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=[1, 2, 'слово'])
        self.assertEqual(u.get_query_data()['foo'], 'слово')
        self.assertEqual(u.get_query_data().getlist('foo'), [1, 2, 'слово'])

    def test_update_query_data_with_correct_escaping(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo='space here!')
        self.assertEqual(u.query_string, 'foo=space+here%21&bar=2')

    def test_update_query_data_with_correct_escaping_unicode(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo='два слова!')
        self.assertEqual(u.query_string,
                         'foo=%D0%B4%D0%B2%D0%B0+%D1%81%D0%BB%D0%BE%D0%B2%D0%B'
                         '0%21&bar=2')

    def test_get_query_string_after_modification(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo=2)
        self.assertEqual(u.get_query_string(), 'foo=2&bar=2')

    def test_get_query_string_after_modification_unicode(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        u.update_query_data(foo='слово')
        self.assertEqual(u.get_query_string(),
                         'foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE&bar=2')

    def test_get_query_with_multiple_values(self):
        u = UrlHelper('/foo')
        u.update_query_data(foo=[1, 2, 3])
        self.assertEqual(u.get_query_string(), 'foo=1&foo=2&foo=3')

    def test_get_query_with_multiple_values_unicode(self):
        u = UrlHelper('/foo')
        u.update_query_data(foo=[1, 2, 'слово'])
        self.assertEqual(u.get_query_string(),
                         'foo=1&foo=2&foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE')

    def test_safe_slash_argument(self):
        u = UrlHelper('/foo')
        u.update_query_data(redir='/foo/bar/')
        self.assertEqual(u.get_query_string(safe='/'), 'redir=/foo/bar/')

    def test_with_query_params_in_url(self):
        u = UrlHelper('/foo')
        u.update_query_data(redir='/foo/bar/?q=Mickey+Mouse')
        self.assertEqual(u.get_query_string(safe='/'),
                         'redir=/foo/bar/%3Fq%3DMickey%2BMouse')

    def test_with_query_params_in_url_unicode(self):
        # FIXME: This breaks. See issue #4
        # https://bitbucket.org/monwara/django-url-tools/issue/4/
        u = UrlHelper('/foo')
        u.update_query_data(redir='/foo/bar/?q=два+слова')
        self.assertEqual(u.get_query_string(safe='/'),
                         'redir=/foo/bar/%3Fq%3D%D0%B4%D0%B2%D0%B0%2B%D1%81%D0%BB%D0')

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

    def test_full_path_with_unicode_query_param(self):
        u = UrlHelper('/foo')
        u.update_query_data(foo='слово')
        self.assertEqual(u.get_full_path(),
                         '/foo?foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE')

    def test_full_path_with_unicode_query_param_2(self):
        u = UrlHelper('/foo?foo=слово')
        u.update_query_data(bar='слово')
        self.assertEqual(u.get_full_path(),
                         '/foo?foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE&bar=%D1%81'
                         '%D0%BB%D0%BE%D0%B2%D0%BE')

    def test_retains_fragment(self):
        u = UrlHelper('/foo#bar')
        u.update_query_data(foo=1)
        self.assertEqual(u.get_full_path(), '/foo?foo=1#bar')

    def test_retains_fragment_unicode(self):
        u = UrlHelper('/foo#bar')
        u.update_query_data(foo='слово')
        self.assertEqual(u.get_full_path(),
                         '/foo?foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE#bar')

    def test_query_property(self):
        u = UrlHelper('/foo?foo=1')
        self.assertEqual(u.query['foo'], '1')

    def test_query_property_unicode(self):
        u = UrlHelper('/foo?foo=слово')
        self.assertEqual(u.query['foo'], 'слово')

    def test_query_setter(self):
        u = UrlHelper('/foo')
        u.query = dict(foo=1)
        self.assertEqual(u.query['foo'], 1)

    def test_query_setter_unicode(self):
        u = UrlHelper('/foo')
        u.query = dict(foo='слово')
        self.assertEqual(u.query['foo'], 'слово')

    def test_query_setter_with_string(self):
        u = UrlHelper('/foo')
        u.query = 'foo=1&bar=2'
        self.assertEqual(u.query['foo'], '1')
        self.assertEqual(u.query['bar'], '2')

    def test_query_setter_with_string_unicode(self):
        u = UrlHelper('/foo')
        u.query = 'foo=слово&bar=2'
        self.assertEqual(u.query['foo'], 'слово')
        self.assertEqual(u.query['bar'], '2')

    def test_query_string_property(self):
        u = UrlHelper('/foo?foo=1&bar=2')
        self.assertEqual(u.query_string, 'foo=1&bar=2')

    def test_query_string_property_unicode(self):
        u = UrlHelper('/foo?foo=слово&bar=2')
        self.assertEqual(u.query_string,
                         'foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE&bar=2')

    def test_query_string_setter(self):
        u = UrlHelper('/foo')
        u.query_string = 'foo=1&bar=2'
        self.assertEqual(u.query['foo'], '1')
        self.assertEqual(u.query['bar'], '2')

    def test_query_string_setter_unicode(self):
        u = UrlHelper('/foo')
        u.query_string = 'foo=слово&bar=2'
        self.assertEqual(u.query['foo'], 'слово')
        self.assertEqual(u.query['bar'], '2')

    def test_get_full_quoted_path(self):
        u = UrlHelper('/foo/bar?foo=1&bar=2#foo')
        self.assertEqual(u.get_full_quoted_path(),
                         '/foo/bar%3Ffoo%3D1%26bar%3D2%23foo')

    def test_get_full_quoted_path_unicode(self):
        u = UrlHelper('/foo/bar?foo=слово&bar=2#foo')
        self.assertEqual(u.get_full_quoted_path(),
                         '/foo/bar%3Ffoo%3D%25D1%2581%25D0%25BB%25D0%25BE%25D0'
                         '%25B2%25D0%25BE%26bar%3D2%23foo')

    def test_use_as_string(self):
        u = UrlHelper('/foo/bar')
        u.query = dict(foo=1, bar=2)
        u.fragment = 'baz'
        self.assertEqual(str(u), '/foo/bar?foo=1&bar=2#baz')

    def test_use_as_string_unicode(self):
        u = UrlHelper('/foo/bar')
        u.query = dict(foo='слово', bar=2)
        u.fragment = 'baz'
        self.assertEqual(str(u),
                         '/foo/bar?foo=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE&bar=2#'
                         'baz')

    def test_use_with_URL_as_param_value(self):
        u = UrlHelper('/foo/bar/')
        u.query = {'redir': '/foo/bar/baz?test=1'}
        self.assertEqual(u.get_full_path(),
                         '/foo/bar/?redir=%2Ffoo%2Fbar%2Fbaz%3Ftest%3D1')

    def test_use_with_URL_as_param_value_unicode(self):
        u = UrlHelper('/foo/bar/')
        u.query = {'redir': '/foo/bar/baz?test=слово'}
        self.assertEqual(u.get_full_path(),
                         '/foo/bar/?redir=%2Ffoo%2Fbar%2Fbaz%3Ftest%3D'
                         '%D1%81%D0%BB%D0%BE%D0%B2%D0%BE')

    def test_hashing_basically_works(self):
        u = UrlHelper('/foo/bar/')
        self.assertEqual(u.hash, '1c184f3891344400380281315d9e7388')

    def test_hashling_with_query_string(self):
        u = UrlHelper('/foo/bar')
        u.query = dict(foo=1)
        self.assertEqual(u.hash, '06f0a42bdd474f053fb1343165a31d42')

    def test_delete_key(self):
        u = UrlHelper('/foo/bar?foo=1&bar=2')
        u.del_param('foo')
        self.assertEqual(u.get_full_path(), '/foo/bar?bar=2')

    def test_delete_key_unicode(self):
        u = UrlHelper('/foo/bar?foo=слово&bar=2')
        u.del_param('foo')
        self.assertEqual(u.get_full_path(), '/foo/bar?bar=2')

    def test_delete_multiple_keys(self):
        u = UrlHelper('/foo/bar?foo=1&bar=2')
        u.del_params('foo', 'bar')
        self.assertEqual(u.get_full_path(), '/foo/bar')

    def test_delete_multiple_keys_unicode(self):
        u = UrlHelper('/foo/bar?foo=слово&bar=2')
        u.del_params('foo', 'bar')
        self.assertEqual(u.get_full_path(), '/foo/bar')

    def test_delete_fails_silently(self):
        u = UrlHelper('/foo/bar?foo=1&bar=2')
        u.del_params('foo', 'baz')  # baz doesn't exist
        self.assertEqual(u.get_full_path(), '/foo/bar?bar=2')

    def test_delete_fails_silently_unicode(self):
        u = UrlHelper('/foo/bar?foo=слово&bar=2')
        u.del_params('foo', 'baz')  # baz doesn't exist
        self.assertEqual(u.get_full_path(), '/foo/bar?bar=2')

    def test_delete_multiple_without_arguments(self):
        u = UrlHelper('/foo/bar?foo=1&bar=2')
        u.del_params()
        self.assertEqual(u.get_full_path(), '/foo/bar')

    def test_overload_param(self):
        u = UrlHelper('/foo/bar?foo=1')
        u.overload_params(foo=2)
        self.assertEqual(u.get_full_path(), '/foo/bar?foo=1&foo=2')

    def test_overload_param_unicode(self):
        u = UrlHelper('/foo/bar?foo=1')
        u.overload_params(foo='слово')
        self.assertEqual(u.get_full_path(), '/foo/bar?foo=1&foo=%D1%81%D0%BB'
                         '%D0%BE%D0%B2%D0%BE')

    def test_url_helper_instance_as_argument(self):
        u1 = UrlHelper('/foo/bar?foo=1&bar=2')
        u2 = UrlHelper(u1)
        self.assertEqual(u2.get_full_path(), '/foo/bar?foo=1&bar=2')

    def test_toggle_params_disable(self):
        u = UrlHelper('/foo/bar?foo=1')
        u.toggle_params(foo=1)
        self.assertEqual(u.get_full_path(), '/foo/bar')

    def test_toggle_params_disable_unicode(self):
        u = UrlHelper('/foo/bar?foo=слово')
        u.toggle_params(foo='слово')
        self.assertEqual(u.get_full_path(), '/foo/bar')

    def test_toggle_params_enable(self):
        u = UrlHelper('/foo/bar?foo=1')
        u.toggle_params(bar=1)
        self.assertEqual(u.get_full_path(), '/foo/bar?foo=1&bar=1')

    def test_toggle_params_enable_unicode(self):
        u = UrlHelper('/foo/bar?foo=1')
        u.toggle_params(bar='слово')
        self.assertEqual(u.get_full_path(), '/foo/bar?foo=1&bar='
                         '%D1%81%D0%BB%D0%BE%D0%B2%D0%BE')

    def test_toggle_params_toggle_multiple(self):
        u = UrlHelper('/foo/bar?foo=1')
        u.toggle_params(foo=1, bar=1)
        self.assertEqual(u.get_full_path(), '/foo/bar?bar=1')

    def test_toggle_params_toggle_multiple_unicode(self):
        u = UrlHelper('/foo/bar?foo=слово')
        u.toggle_params(foo='слово', bar=1)
        self.assertEqual(u.get_full_path(), '/foo/bar?bar=1')
