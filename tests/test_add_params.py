from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from url_tools.templatetags.urls import add_params


class AddParamsTestCase(TestCase):
    def test_add_params_basicaly_works(self):
        self.assertEqual(
            add_params('/foo/bar?baz=0#frag', foo=1, bar=2),
            '/foo/bar?bar=2&foo=1&baz=0#frag'
        )
