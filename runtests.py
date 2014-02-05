#!/usr/bin/env python

import sys
from os.path import dirname, abspath

from django.conf import settings

from nose.plugins.plugintest import run_buffered as run


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '%s/test.db' % dirname(abspath(__file__)),
            }
        },
        INSTALLED_APPS=[
            'url_tools',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
    )


def runtests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['tests']

    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    run(argv=sys.argv)

if __name__ == '__main__':
    runtests()
