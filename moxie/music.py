import ConfigParser
import StringIO
import codecs
import glob
import os.path
import subprocess

class TrackList(dict):
    """A dictionary with keys as MP3 files and values as TrackInfo instances."""

    HEADER = 'README'

    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise IOError("%s not a directory" % directory)

        self.directory = directory

        try:
            header = [line.strip()
                      for line in codecs.open(os.path.join(directory, self.HEADER), encoding='utf-8').readlines()]
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
        self.album = 'No Album'
        self.artist = 'No Artist'
        self.duration = '?:??'
        self.length = 0
        self.title = 'No Title'
        self.size = 0

        self._load(filename)

    def _load(self, filename):
        if not os.path.isfile(filename):
            raise IOError(filename)

        output = subprocess.check_output([
            'ffprobe',
            '-loglevel', '8',
            '-show_format',
            '-print_format', 'ini',
            filename])

        probe = ConfigParser.SafeConfigParser()
        probe.readfp(StringIO.StringIO(output))

        if probe.has_section('format.tags'):
            self.album = probe.get('format.tags', 'album') or 'No Album'
            self.artist = probe.get('format.tags', 'artist') or 'No Artist'
            self.title = probe.get('format.tags', 'title') or 'No Title'

        self.length = probe.getfloat('format', 'duration')
        self.duration = "%u:%.2d" % (self.length / 60, self.length % 60)
        self.size = probe.getint('format', 'size')
