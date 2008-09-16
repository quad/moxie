#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'moxie',
    version = '8.10',

    packages = find_packages(),
    package_data = {
        'moxie': ['templates/*', 'static/*'],
    },

    install_requires = [
        'flup >= 1.0',
        'Mako >= 0.2.2',
        'Markdown >= 1.6',
        'mutagen >= 1.14',
        'selector',
        'WebOb >= 0.9.3',
    ],
    dependency_links = [
        # mutagen
        "http://code.google.com/p/quodlibet/downloads/list",
    ],

    entry_points = {
        'console_scripts': [
            'moxie-test = moxie.deploy:local',
        ]
    },

    test_suite = 'nose.collector',
)
