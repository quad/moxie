import codecs
import glob
import os
import os.path

import mutagen
import mutagen.easyid3
import mutagen.id3

class TrackList(dict):
    """A dictionary with keys as MP3 files and values as TrackInfo instances."""

    HEADER = 'README'

    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise IOError("%s not a directory" % directory)

        self.directory = directory

        try:
            header = [line.strip()
                      for line in codecs.open(os.path.join(directory, self.HEADER)).readlines()]
        except IOError:
            self.title = "A Moxie Mixtape!"
            self.subtitle = "Make a README"
        else:
            print header
            self.title = header[0]
            self.subtitle = '\n'.join(header[1:])

        for fn in glob.glob(os.path.join(directory, '*.mp3')):
            self[os.path.basename(fn)] = TrackInfo(fn)

class TrackInfo:
    """Metadata for audio files."""

    def __init__(self, filename):
        self.album = 'No Album'
        self.artist = 'No Artist'
        self.duration = '?:??'
        self.length = 0
        self.title = 'No Title'
        self.size = 0

        self._load(filename)

    def _load(self, filename):
        short_tags = full_tags = mutagen.File(filename)

        if isinstance(full_tags, mutagen.mp3.MP3):
            short_tags = mutagen.mp3.MP3(filename, ID3 = mutagen.easyid3.EasyID3)

        self.album = short_tags.get('album', ['No Album'])[0]
        self.artist = short_tags.get('artist', ['No Artist'])[0]
        self.duration = "%u:%.2d" % (full_tags.info.length / 60, full_tags.info.length % 60)
        self.length = full_tags.info.length
        self.title = short_tags.get('title', ['No Title'])[0]
        self.size = os.stat(filename).st_size
