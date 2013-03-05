from __future__ import absolute_import, unicode_literals

from django import template

from ..helper import UrlHelper

register = template.Library()


@register.assignment_tag
def url_params(url, **kwargs):
    u = UrlHelper(url)
    u.update_query_data(**kwargs)
    return u.get_full_path()

