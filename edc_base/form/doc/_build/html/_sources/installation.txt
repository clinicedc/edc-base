Installation
============

Checkout the latest version of :mod:`bhp_base_form` into your project folder::

    svn co http://192.168.1.50/svn/bhp_base_form


Add :mod:`bhp_base_form` to your project ''settings'' file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django_extensions',
        'audit_trail',
        'bhp_base_model',
        'bhp_common',
        'bhp_base_form',
        ...
        )
    
        