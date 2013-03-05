from unittest import TestCase

from mock import Mock

from url_tools.context_processors import CurrentUrlProcessor


class CurrentUrlProcessorTestCase(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.get_full_path.return_value = '/foo?foo=1'
        self.response = Mock()
        self.response.context_data = {}

    def test_can_get_url_from_request(self):
        c = CurrentUrlProcessor()
        c.process_template_response(self.request, self.response)
        self.assertTrue(self.request.get_full_path.called)

    def test_can_insert_url_helper_into_context(self):
        c = CurrentUrlProcessor()
        c.process_template_response(self.request, self.response)

        self.assertTrue('current_url' in self.response.context_data)
        self.assertEqual(
            self.response.context_data['current_url'].get_full_path(),
            self.request.get_full_path.return_value
        )
