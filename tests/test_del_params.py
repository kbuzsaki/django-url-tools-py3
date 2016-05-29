

from unittest import TestCase

from url_tools.templatetags.urls import del_params
from url_tools.helper import UrlHelper


class DelParamsTestCase(TestCase):
    def test_del_params_basic(self):
        self.assertEqual(
            del_params('/foo?bar=1&baz=2', 'baz'),
            '/foo?bar=1'
        )

    def test_del_paramss_all(self):
        self.assertEqual(
            del_params('/foo?bar=1&baz=2'),
            '/foo'
        )

    def test_del_params_takes_helper_instance(self):
        self.assertEqual(
            del_params(UrlHelper('/foo?bar=1&baz=2'), 'bar'),
            '/foo?baz=2'
        )
