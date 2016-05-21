import subprocess

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
    def __init__(self, in_fd, info, out_fn):
        params = ['lame']
        params += ['--quiet']
        params += ['-V6']
        params += ['--tt', info.title]
        params += ['--ta', info.artist]
        params += ['--tl', info.album]
        params += ['-', out_fn]
        subprocess.Popen.__init__(self, params, stdin=in_fd)

class FFLame(Transcoder):
    """FFMpeg and LAME based transcoder from variable formats to streamable MP3s."""

    FFMPEG = 'ffmpeg -loglevel warning'

    def __init__(self, fn_source, fn_sink):
        Transcoder.__init__(self, fn_source, fn_sink)

        self.info = TrackInfo(fn_source)

    def run(self):
        ffmpeg = FFmpeg(self.fn_source)
        lame = LAME(ffmpeg.stdout, self.info, self.fn_sink)
        ffmpeg.stdout.close()

        errors = []

        if lame.wait():
            errors.append('LAME') 

        if ffmpeg.wait():
            errors.append('FFMPEG') 

        if errors:
            print "%s -> %s FAILED (%s)" % (self.fn_source, self.fn_sink, ', '.join(errors))
        else:
            print "%s -> %s" % (self.fn_source, self.fn_sink)
