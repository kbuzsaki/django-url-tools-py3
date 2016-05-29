

from unittest import TestCase

from url_tools.templatetags.urls import add_params
from url_tools.helper import UrlHelper


class AddParamsTestCase(TestCase):
    def test_add_params_basicaly_works(self):
        self.assertEqual(
            add_params('/foo/bar?baz=0#frag', foo=1, bar=2),
            '/foo/bar?baz=0&bar=2&foo=1#frag'
        )

    def test_add_parasm_with_helper_instance(self):
        self.assertEqual(
            add_params(UrlHelper('/foo/bar?baz=0#frag'), foo=1, bar=2),
            '/foo/bar?baz=0&bar=2&foo=1#frag'
        )
