#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-admin-extensions',
    version="0.1.0",
    description='Simple tools to extend the django admin site',
    author='Ionata Web Solutions',
    author_email='webmaster@ionata.com.au',
    url='https://bitbucket.org/ionata/django-admin-extensions',
    packages=['adminextensions'],
    install_requires=['Django>=1.4'],
    package_data={},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
