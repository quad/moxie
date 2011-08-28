import os

class Transcoder:
    """Audio transcoder from variable formats to streamable MP3s."""

    def __init__(self, fn_source, fn_sink):
        self.fn_source = os.path.abspath(fn_source)
        self.fn_sink = os.path.abspath(fn_sink)

        assert(os.path.exists(self.fn_source))
        assert(not os.path.exists(self.fn_sink))

    def run(self):
        raise NotImplementedError
