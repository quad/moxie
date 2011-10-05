import subprocess

from mutagen.easyid3 import EasyID3

from moxie.music import TrackInfo
from moxie.transcode.base import Transcoder

class FFmpeg(subprocess.Popen):
    def __init__(self, in_fn):
        params = ['ffmpeg']
        params += '-loglevel warning'.split()
        params += ['-i', in_fn]
        params += ['-f', 'wav']
        params += ['-']
        subprocess.Popen.__init__(self, params, stdout=subprocess.PIPE)

class LAME(subprocess.Popen):
    def __init__(self, in_fd, out_fn):
        params = ['lame']
        params += ['--quiet']
        params += ['-V6']
        params += ['--tt', 'null']
        params += ['--ta', 'null']
        params += ['--tl', 'null']
        params += ['-', out_fn]
        subprocess.Popen.__init__(self, params, stdin=in_fd)

class ID3(EasyID3):
    def apply(self, track_info):
        self['title'] = track_info.title
        self['artist'] = track_info.artist
        self['album'] = track_info.album

class FFLame(Transcoder):
    """FFMpeg and LAME based transcoder from variable formats to streamable MP3s."""

    FFMPEG = 'ffmpeg -loglevel warning'

    def __init__(self, fn_source, fn_sink):
        Transcoder.__init__(self, fn_source, fn_sink)

        self.info = TrackInfo(fn_source)

    def run(self):
        ffmpeg = FFmpeg(self.fn_source)
        lame = LAME(ffmpeg.stdout, self.fn_sink)
        ffmpeg.stdout.close()

        errors = []

        if lame.wait():
            errors.append('LAME') 

        if ffmpeg.wait():
            errors.append('FFMPEG') 

        id3 = ID3(self.fn_sink)
        id3.apply(self.info)
        id3.save()

        if errors:
            print "%s -> %s FAILED (%s)" % (self.fn_source, self.fn_sink, ', '.join(errors))
        else:
            print "%s -> %s" % (self.fn_source, self.fn_sink)
