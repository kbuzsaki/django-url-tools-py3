

from unittest import TestCase

from url_tools.templatetags.urls import overload_params


class overloadParamsTestCase(TestCase):
    def test_overload_params_basic(self):
        self.assertEqual(
            overload_params('/search/?q=something&selected_facets=second%3Abar',
                           selected_facets='first:foo'),
            '/search/?q=something&selected_facets=second%3Abar&selected_facets=first%3Afoo'
        )

    def test_overload_params_duplicate(self):
        self.assertEqual(
            overload_params('/search/?q=something&selected_facets=second%3Abar&selected_facets=first%3Afoo',
                           selected_facets='first:foo'),
            '/search/?q=something&selected_facets=second%3Abar&selected_facets=first%3Afoo'
        )