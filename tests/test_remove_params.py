from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from url_tools.templatetags.urls import remove_params
from url_tools.helper import UrlHelper


class RemoveParamsTestCase(TestCase):
    def test_remove_params_basic(self):
        self.assertEqual(
            remove_params('/search/?q=something&selected_facets=first:foo&selected_facets=second:bar', selected_facets='first'),
            '/search/?q=something&selected_facets=second%3Abar'
        )

    def test_remove_params_takes_helper_instance(self):
        self.assertEqual(
            remove_params(UrlHelper('/search/?q=something&selected_facets=first:foo&selected_facets=second:bar'), selected_facets='first'),
            '/search/?q=something&selected_facets=second%3Abar'
        )
        

