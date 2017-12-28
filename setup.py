from distutils.core import setup

setup(
    name='django-url-tools-py3',
    description='Django helpers for dealing with URLs in templates',
    version='0.2.0',
    packages=['url_tools', 'url_tools.templatetags'],
    author='Monwara LLC',
    author_email='branko@monwara.com',
    maintainer='Kyle Buzsaki',
    maintainer_email='kbuzsaki@gmail.com',
    url='https://github.com/kbuzsaki/django-url-tools-py3',
    download_url='https://github.com/kbuzsaki/django-url-tools-py3/releases',
    license='BSD',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
)


