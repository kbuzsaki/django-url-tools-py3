from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from url_tools.templatetags.urls import toggle_params


class toggleParamsTestCase(TestCase):
    def test_toggle_params_basic(self):
        self.assertEqual(toggle_params('/foo/?foo=1', foo=1), '/foo/')

    def test_toggle_params_multiple(self):
        self.assertEqual(toggle_params('/foo/?foo=1', foo=1, bar=2), '/foo/?bar=2')
