import glob
import os.path

import mutagen
import mutagen.easyid3
import mutagen.id3

FN_HEADER = 'README'

class Directory:
    def __init__(self, directory):
        try:
            self.header = file(os.path.join(directory, FN_HEADER)).read()
        except IOError:
            self.header = None

        self.tracks = {}
        for fn in sorted(glob.glob(os.path.join(directory, '*.mp3'))):
            self.tracks[fn] = TrackInfo(fn)

class TrackInfo:
    def __init__(self, filename):
        try:
            self.load(filename)
        except mutagen.id3.error:
            self.artist = "No Artist"
            self.title = "No Title"
            self.duration = "?:??"
 
    def load(self, filename):
        short_tags = full_tags = mutagen.File(filename)
 
        if isinstance(full_tags, mutagen.mp3.MP3):
            short_tags = mutagen.easyid3.EasyID3(filename)
 
        self.artist = short_tags['artist'][0]
        self.title = short_tags['title'][0]
        self.duration = "%u:%.2d" % (full_tags.info.length / 60, full_tags.info.length % 60)
