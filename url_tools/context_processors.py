from __future__ import absolute_import, unicode_literals

from .helper import UrlHelper


class CurrentUrlProcessor(object):
    def process_template_response(self, request, response):
        full_path = request.get_full_path()
        response.context_data['current_url'] = UrlHelper(full_path)
        return response
