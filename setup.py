# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages
from os.path import join, abspath, normpath, dirname

with open(join(dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(join(dirname(__file__), 'VERSION')) as f:
    VERSION = f.read()

tests_require = []
with open(join(dirname(abspath(__file__)), 'requirements.txt')) as f:
    for line in f:
        tests_require.append(line.strip())

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))
setup(
    name='edc-base',
    version=VERSION,
    author=u'Erik van Widenfelt',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/clinicedc/edc-base',
    license='GPL license, see LICENSE',
    description='Base mixins and utilities for clinicedc/edc projects.',
    long_description=README,
    zip_safe=False,
    keywords='django base models fields forms admin',
    install_requires=[
        'arrow',
        'django',
        'django-environ',
        'django-extensions',
        'django-js-reverse',
        'django-logentry-admin',
        'django-simple-history>=2.7.0',
        'django-crypto-fields',
        'django-revision',
        'edc-constants',
        'edc-device',
        'edc-model-fields',
        'edc-navbar',
        'edc-protocol',
        'mysqlclient',
        # 'psycopg2-binary',
        'python-dateutil',
        'python-memcached',
        'pytz',
        'tqdm',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.7",
    tests_require=tests_require,
    test_suite='runtests.main',
)
