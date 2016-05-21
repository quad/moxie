# -*- coding: utf-8 -*-

import glob
import os.path
import tempfile
import unittest

from tests import DATA

from moxie.music import TrackList, TrackInfo

class TrackListTests(unittest.TestCase):
    """TrackListTest tests."""

    def test_not_found(self):
        """A file that doesn't exist."""

        with tempfile.NamedTemporaryFile() as fn, \
                self.assertRaises(IOError):
            TrackList(fn.name)

    def test_simple(self):
        """Load a simple directory."""

        tracks = TrackList(DATA)

        self.assertEqual(tracks.title, "A Moxie Mixtape!")
        self.assertEqual(tracks.subtitle, "Make a README")

        for fn in glob.glob(os.path.join(DATA, '*.mp3')):
            self.assertIn(os.path.basename(fn), tracks)

    def test_filename_purity(self):
        """TrackList uses filenames as keys."""

        tracks = TrackList(DATA)

        for fn in tracks:
            self.assertEqual(fn, os.path.basename(fn))

class TrackListHeaderTest(unittest.TestCase):
    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.headername = os.path.join(self.dirname, TrackList.HEADER)

        self.header = u"Hello! 嘴上无毛，办事不牢"

        with file(self.headername, 'w') as f:
            f.write(self.header.encode('utf-8'))

    def tearDown(self):
        os.unlink(self.headername)
        os.rmdir(self.dirname)

    def test_only_header(self):
        """Only with a header."""

        tracks = TrackList(self.dirname)

        self.assertEqual(tracks.title, self.header)
        self.assertEqual(tracks.subtitle, '')
        self.assertEqual(len(tracks), 0)

class TrackInfoNegativeTests(unittest.TestCase):
    """TrackInfo tests on non-existent data."""

    def test_invalid(self):
        """An invalid file."""

        with tempfile.NamedTemporaryFile() as fn, \
                self.assertRaises(IOError):
            TrackInfo(fn.name)

    def test_nonexistant(self):
        """A non-existent file."""

        with self.assertRaises(IOError):
            TrackInfo(os.path.join(DATA, 'xyzzy'))

    def test_invalid_directory(self):
        """A 'mp3' that is a directory."""

        with self.assertRaises(IOError):
            TrackInfo(DATA)

class TrackInfoDataTests(unittest.TestCase):
    """TrackInfo tests on prepared data."""

    NULL_MP3 = os.path.join(DATA, 'null-noid3.mp3')
    V1_MP3   = os.path.join(DATA, 'null-v1.mp3')
    V2_MP3   = os.path.join(DATA, 'null-v2.mp3')

    def test_v1(self):
        """An ID3v1 tagged file."""

        info = TrackInfo(self.V1_MP3)
        self.check_tags(info)

    def test_v2(self):
        """An ID3v2 tagged file."""

        info = TrackInfo(self.V2_MP3)
        self.check_tags(info)

    def test_none(self):
        """An untagged file."""

        info = TrackInfo(self.NULL_MP3)

        self.assertEqual(info.album, 'No Album')
        self.assertEqual(info.artist, 'No Artist')
        self.assertEqual(info.title, 'No Title')

    def check_tags(self, info):
        self.assertEqual(info.album, 'Null Album')
        self.assertEqual(info.artist, 'Null Artist')
        self.assertEqual(info.title, 'Null Title')

        self.check_info(info)

    def check_info(self, info):
        self.assertEqual(info.duration, '0:00')
        self.assertLess(info.length, 1)
        self.assertGreater(info.size, 0)
