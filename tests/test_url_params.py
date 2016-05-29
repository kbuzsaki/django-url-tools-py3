

from unittest import TestCase

from url_tools.templatetags.urls import url_params


class UrlParamsTestCase(TestCase):
    def test_url_params_basically_works(self):
        self.assertEqual(
            url_params('/foo?foo=1', bar='2'),
            '/foo?foo=1&bar=2'
        )

    def test_can_override_existing_params(self):
        self.assertEqual(
            url_params('/foo?foo=1', foo='2'),
            '/foo?foo=2'
        )
