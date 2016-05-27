# -*- coding: utf-8 -*-

import contextlib
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

    def test_uris(self):
        """Sanity check the URIs."""

        uris = [uri for uri, func in moxie.web.uri.uris(self.app)]

        self.assertIn('', uris)
        self.assertGreater(len(uris), 1)

    def test_dynamic(self):
        """Dynamic requests."""

        for uri, func in moxie.web.uri.uris(self.app):
            print uri

            req = webob.Request.blank('/' + uri)
            res = req.get_response(self.app)

            self.assertEqual(res.status, '200 OK')

    def test_static(self):
        """Static requests."""

        for fn in pkg_resources.resource_listdir(moxie.__name__, 'static/'):
            print fn

            req = webob.Request.blank('/' + fn)
            res = req.get_response(self.app)

            self.assertEqual(res.status, '200 OK')

    def test_music(self):
        """Music requests."""

        for fn in glob.glob(os.path.join(DATA, '*.mp3')):
            fn = os.path.basename(fn)

            print fn

            req = webob.Request.blank('/' + urllib.quote(fn))
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

@contextlib.contextmanager
def tempdir():
    dn = tempfile.mkdtemp()
    try:
        yield dn
    finally:
        shutil.rmtree(dn)

class DeployTest(unittest.TestCase):
    def test_template(self):
        with tempdir() as output_directory:
            moxie.web.deploy('/', DATA, output_directory)

            self.assertTrue(os.path.isfile(os.path.join(output_directory, 'index.html')))

    def test_static(self):
        with tempdir() as output_directory:
            moxie.web.deploy('/', DATA, output_directory)

            self.assertTrue(os.path.isfile(os.path.join(output_directory, 'moxie.js')))

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
