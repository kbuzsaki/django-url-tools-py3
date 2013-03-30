from __future__ import absolute_import, unicode_literals

import urllib

from django import template

from ..helper import UrlHelper

register = template.Library()


@register.simple_tag
def add_params(url, **kwargs):
    if type(url) == UrlHelper:
        url = url.get_full_path()
    url = UrlHelper(url)
    try:
        url.update_query_data(**kwargs)
        return url.get_full_path()
    except:
        return ''


@register.simple_tag
def del_params(url, *args):
    if type(url) == UrlHelper:
        url = url.get_full_path()
    url = UrlHelper(url)
    try:
        url.del_params(*args)
        return url.get_full_path()
    except:
        return ''


@register.assignment_tag
def url_params(url, **kwargs):
    u = UrlHelper(url)
    u.update_query_data(**kwargs)
    return u.get_full_path()


@register.filter(name='quote')
def quote_param(value, safe='/'):
    return urllib.quote(value, safe)


@register.filter(name='quote_plus')
def quote_param_plus(value, safe='/'):
    return urllib.quote_plus(value, safe)
