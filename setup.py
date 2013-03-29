from distutils.core import setup

setup(
    name='django-url-tools',
    description='Django helpers for dealing with URLs in templates',
    long_description=open('README.rst').read(),
    version='0.0.3',
    packages=['url_tools', 'url_tools.templatetags'],
    author='Monwara LLC',
    author_email='branko@monwara.com',
    url='https://bitbucket.org/monwara/django-url-tools',
    download_url='https://bitbucket.org/monwara/django-url-tools/downloads',
    license='BSD',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
)


