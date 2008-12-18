#!/usr/bin/env python

try:
    import pygst
    pygst.require('0.10')
except ImportError:
    logging.info('GStreamer bindings should be installed: http://pygstdocs.berlios.de/')

from setuptools import setup, find_packages

setup(
    name = 'moxie',
    version = '8.12',
    maintainer = 'Scott Robinson',
    maintainer_email = 'scott@quadhome.com',
    description = 'Makes mixtapes!',
    download_url = 'http://github.com/quad/moxie',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'Topic :: Utilities',
    ],

    packages = find_packages(),
    package_data = {
        'moxie': ['templates/*', 'static/*'],
    },

    install_requires = [
        'flup', # BSD
        'Mako', # MIT
        'Markdown >= 1.7', # BSD
        'mutagen >= 1.15', # GPLv2
        'selector', # LGPLv2.1
        'static', # LGPLv2.1
        'WebOb', # MIT
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
