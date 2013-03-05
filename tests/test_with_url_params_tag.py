from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from url_tools.templatetags.urls import with_url_params


class WithUrlParamsTestCase(TestCase):
    def test_with_url_params_basically_works(self):
        self.assertEquals(
            with_url_params('/foo?foo=1', bar='2'),
            '/foo?foo=1&bar=2'
        )

    def test_can_override_existing_params(self):
        self.assertEqual(
            with_url_params('/foo?foo=1', foo='2'),
            '/foo?foo=2'
        )
