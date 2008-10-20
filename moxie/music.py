import glob
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
                      for line in file(os.path.join(directory, self.HEADER)).readlines()]
        except IOError:
            self.title = "A Moxie Mixtape!"
            self.subtitle = "Make a README"
        else:
            self.title = header[0]
            self.subtitle = '\n'.join(header[1:])

        for fn in glob.glob(os.path.join(directory, '*.mp3')):
            self[os.path.basename(fn)] = TrackInfo(fn)

class TrackInfo:
    """Metadata for audio files."""

    def __init__(self, filename):
        try:
            self._load(filename)
        except mutagen.id3.error:
            self.album = 'No Album'
            self.artist = 'No Artist'
            self.duration = '?:??'
            self.length = 0
            self.title = 'No Title'

    def _load(self, filename):
        short_tags = full_tags = mutagen.File(filename)

        if isinstance(full_tags, mutagen.mp3.MP3):
            short_tags = mutagen.easyid3.EasyID3(filename)

        self.album = short_tags['album'][0]
        self.artist = short_tags['artist'][0]
        self.duration = "%u:%.2d" % (full_tags.info.length / 60, full_tags.info.length % 60)
        self.length = full_tags.info.length
        self.title = short_tags['title'][0]
