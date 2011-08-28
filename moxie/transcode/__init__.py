try:
    from moxie.transcode.gst import Gst as Transcoder
except ImportError:
    from moxie.transcode.fflame import FFLame as Transcoder
