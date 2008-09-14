#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name = 'moxie',
  version = '0.1',
  packages = find_packages(),

  install_requires = [
    'web.py >= 0.23',
    'mutagen >= 1.11',
  ],

  test_suite = 'nose.collector'
)
