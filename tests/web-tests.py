# -*- coding: utf-8 -*-

import glob
import os.path
import shutil
import tempfile
import unittest
import urllib

import pkg_resources

import webob

from tests import DATA

import moxie.web

class MoxieTests(unittest.TestCase):
    """Moxie WSGI tests."""

    def setUp(self):
        self.app = moxie.web.app(DATA)

    def test_file_ok(self):
        """Exposes a file that exists."""

        req = webob.Request.blank('/index.html')
        res = req.get_response(self.app)

        self.assertEqual(res.status, '200 OK')

    def test_file_exposure(self):
        """Expose files?"""

        req = webob.Request.blank('/null')
        res = req.get_response(self.app)

        self.assertEqual(res.status, '404 Not Found')

    def test_no_local_css(self):
        """No Local CSS"""

        req = webob.Request.blank('/local.css')
        res = req.get_response(self.app)

        self.assertEqual(res.status, '404 Not Found')

class CSSTest(unittest.TestCase):
    def setUp(self):
        self.css_fn = os.path.join(DATA, 'local.css')
        file(self.css_fn, 'w').close()

        self.app = moxie.web.app(DATA)

    def tearDown(self):
        os.unlink(self.css_fn)

    def test_local_css(self):
        """Local CSS"""

        req = webob.Request.blank('/local.css')
        res = req.get_response(self.app)

        self.assertEqual(res.status, '200 OK')

class DeployTest(unittest.TestCase):
    def test_template(self):
        with moxie.web.tempdir() as output_directory:
            moxie.web.deploy('/', DATA, output_directory)

            self.assertTrue(os.path.isfile(os.path.join(output_directory, 'index.html')))

    def test_static(self):
        with moxie.web.tempdir() as output_directory:
            moxie.web.deploy('/', DATA, output_directory)

            self.assertTrue(os.path.isfile(os.path.join(output_directory, 'moxie.js')))

    def test_music(self):
        with moxie.web.tempdir() as output_directory:
            moxie.web.deploy('/', DATA, output_directory)

            self.assertTrue(os.path.isfile(os.path.join(output_directory, 'null-v1.mp3')))

    def test_no_local_css(self):
        with moxie.web.tempdir() as output_directory:
            moxie.web.deploy('/', DATA, output_directory)

            self.assertFalse(os.path.isfile(os.path.join(output_directory, 'local.css')))

    def test_local_css(self):
        try:
            css_fn = os.path.join(DATA, 'local.css')
            file(css_fn, 'w').close()

            with moxie.web.tempdir() as output_directory:
                moxie.web.deploy('/', DATA, output_directory)

                self.assertTrue(os.path.isfile(os.path.join(output_directory, 'local.css')))
        finally:
            os.unlink(css_fn)

class UnicodeTest(unittest.TestCase):
    def setUp(self):
        self.readme_fn = os.path.join(DATA, 'README')
        with file(self.readme_fn, 'w') as f:
            f.write(u'Hello! 嘴上无毛，办事不牢'.encode('utf-8'))

        self.app = moxie.web.app(DATA)

    def tearDown(self):
        os.unlink(self.readme_fn)

    def test_utf8_readme(self):
        """UTF-8 README"""

        req = webob.Request.blank('/')
        res = req.get_response(self.app)

        self.assertEqual(res.status, '200 OK')
