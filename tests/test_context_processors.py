from unittest import TestCase

from mock import Mock

from url_tools.context_processors import current_url


class CurrentUrlProcessorTestCase(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.get_full_path.return_value = '/foo?foo=1'

    def test_can_get_url_from_request(self):
        current_url(self.request)
        self.assertTrue(self.request.get_full_path.called)

    def test_can_insert_url_helper_into_context(self):
        d = current_url(self.request)
        self.assertTrue('current_url' in d)
        self.assertEqual(
            d['current_url'].get_full_path(),
            self.request.get_full_path.return_value
        )
