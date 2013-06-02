from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from url_tools.templatetags.urls import insert_params 
from url_tools.helper import UrlHelper


class InsertParamsTestCase(TestCase):
    def test_insert_params_basic(self):
        self.assertEqual(
            insert_params('/search/?q=something&selected_facets=second%3Abar',
                           selected_facets='first:foo'),
            '/search/?q=something&selected_facets=second%3Abar&selected_facets=first%3Afoo'
        )    
    def test_insert_params_duplicate(self):
        self.assertEqual(
            insert_params('/search/?q=something&selected_facets=second%3Abar&selected_facets=first%3Afoo',
                           selected_facets='first:foo'),
            '/search/?q=something&selected_facets=second%3Abar&selected_facets=first%3Afoo'
        )