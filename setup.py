#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'moxie',
    version = '8.12.1',
    description = 'Makes mixtapes!',
    url = 'http://github.com/quad/moxie',

    author = 'Scott Robinson',
    author_email = 'scott@quadhome.com',

    maintainer = 'Moxie Hackers',
    maintainer_email = 'moxie-hackers@googlegroups.com',

    license = 'GPLv3',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'Topic :: Utilities',
    ],

    packages = ['moxie'],
    include_package_data = True,

    install_requires = [
        'flup', # BSD
        'Mako', # MIT
        'Markdown >= 1.7', # BSD
        'selector', # LGPLv2.1
        'static', # LGPLv2.1
        'WebOb', # MIT
    ],

    entry_points = {
        'console_scripts': [
            'moxie-test = moxie.deploy:local',
            'moxie-static = moxie.deploy:static',
        ]
    },

    test_suite = 'tests',
)
