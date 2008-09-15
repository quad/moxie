#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'moxie',
    version = '8.10',

    packages = find_packages(),
    package_data = {
        '': ['templates/*', 'static/*'],
    },

    install_requires = [
        'web.py >= 0.22',
        'mutagen >= 1.11',
    ],

    entry_points = {
        'console_scripts': [
            'moxie = moxie:main',
        ]
    },

    test_suite = 'nose.collector',
)
