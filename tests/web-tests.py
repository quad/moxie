import glob
import os.path
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

        assert '' in uris
        assert len(uris) > 1

    def test_dynamic(self):
        """Dynamic requests."""

        for uri, func in moxie.web.uri.uris(self.app):
            print uri

            req = webob.Request.blank('/' + uri)
            res = req.get_response(self.app)

            assert res.status == '200 OK'

    def test_static(self):
        """Static requests."""

        for fn in pkg_resources.resource_listdir(moxie.__name__, 'static/'):
            print fn

            req = webob.Request.blank('/' + fn)
            res = req.get_response(self.app)

            assert res.status == '200 OK'

    def test_music(self):
        """Music requests."""

        for fn in glob.glob(os.path.join(DATA, '*.mp3')):
            fn = os.path.basename(fn)

            print fn

            req = webob.Request.blank('/' + urllib.quote(fn))
            res = req.get_response(self.app)

            assert res.status == '200 OK'

    def test_file_exposure(self):
        """Expose files?"""

        req = webob.Request.blank('/' + self.app.music.HEADER)
        res = req.get_response(self.app)

        assert res.status == '404 Not Found'
