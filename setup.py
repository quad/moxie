#!/usr/bin/env python

try:
    import pygst
    pygst.require('0.10')
    import gst
except ImportError:
    logging.error('GStreamer bindings need to be installed: http://pygstdocs.berlios.de/')

from setuptools import setup, find_packages

setup(
    name = 'moxie',
    version = '8.10',

    packages = find_packages(),
    package_data = {
        'moxie': ['templates/*', 'static/*'],
    },

    install_requires = [
        'flup',
        'Mako',
        'Markdown >= 1.7',
        'mutagen >= 1.15',
        'selector',
        'static',
        'WebOb',
    ],
    dependency_links = [
        # mutagen
        "http://code.google.com/p/quodlibet/downloads/list",
    ],

    entry_points = {
        'console_scripts': [
            'moxie-test = moxie.deploy:local',
            'moxie-static = moxie.deploy:static',
        ]
    },

    test_suite = 'nose.collector',
)
