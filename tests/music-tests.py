from __future__ import with_statement

import glob
import os.path
import tempfile
import unittest

from nose.tools import raises

from moxie.music import TrackList, TrackInfo

DATA = os.path.join(os.path.dirname(__file__), 'data')

class TrackListTests(unittest.TestCase):
    """TrackListTest tests."""

    @raises(IOError)
    def test_not_found(self):
        """A directory that doesn't exist."""

        fn = tempfile.mktemp()
        TrackList(fn)

    def test_simple(self):
        """Load a simple directory."""

        tracks = TrackList(DATA)

        assert tracks.header == None

        for fn in glob.glob(os.path.join(DATA, '*.mp3')):
            assert fn in tracks

    def test_only_header(self):
        """Only with a header."""

        header = "# Hello!"
        dirname = tempfile.mkdtemp()

        with file(os.path.join(dirname, TrackList.HEADER), 'w') as f:
            f.write(header)

        tracks = TrackList(dirname)

        assert tracks.header == header
        assert len(tracks) == 0

class TrackInfoTests(unittest.TestCase):
    """TrackInfo tests."""

    @raises(IOError)
    def test_not_found(self):
        """Non-existent MP3."""

        fn = tempfile.mktemp()
        TrackInfo(fn)

    def test_v1(self):
        """An ID3v1 tagged file."""

        info = TrackInfo(os.path.join(DATA, 'null-v1.mp3'))
        self.check_info(info)

    def test_v2(self):
        """An ID3v2 tagged file."""

        info = TrackInfo(os.path.join(DATA, 'null-v2.mp3'))
        self.check_info(info)

    def test_none(self):
        """An untagged file."""

        info = TrackInfo(os.path.join(DATA, 'null-noid3.mp3'))

        assert info.album == 'No Album'
        assert info.artist == 'No Artist'
        assert info.duration == '?:??'
        assert info.length == 0
        assert info.title == 'No Title'

    def check_info(self, info):
        assert info.album == 'Null Album'
        assert info.artist == 'Null Artist'
        assert info.duration == '0:00'
        assert info.title == 'Null Title'

    @raises(IOError)
    def test_invalid_directory(self):
        """A 'mp3' that is a directory."""

        TrackInfo(DATA)
