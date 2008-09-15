import glob
import mimetypes
import os.path
import sys
import urlparse
import xml.etree.ElementTree as ET

import pkg_resources

import web
import mutagen
import mutagen.id3
import mutagen.easyid3

files = sorted(glob.glob('*.mp3'))
render = web.template.render(pkg_resources.resource_filename(__name__, 'templates/'))

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

def tracklist():
    for count, fn in enumerate(files):
        info = TrackInfo(fn)
        url = urlparse.urljoin(web.ctx.homedomain,
                               web.net.urlquote(web.http.url(fn)))

        yield count, info, url

class XSPF:
    def GET(self):
        web.header('Content-Type', 'application/xspf+xml')
        print render.xspf(tracklist())

class Index:
    def GET(self):
        xspf_url = urlparse.urljoin(web.ctx.homedomain, '/xspf')
        print render.index(xspf_url, tracklist())

def leak_file(f):
    while True:
        buf = f.read(16 * 1024)
        if not buf:
            break
        yield buf
    f.close()

class Static:
    def GET(self, filename):
        content_type, encoding = mimetypes.guess_type(filename)
        web.header('Content-Type', content_type)

        # Serve the music.
        if filename in files:
            return leak_file(file(filename))

        # Serve the necessities.
        fn_static = os.path.join('static', filename)

        if pkg_resources.resource_exists(__name__, fn_static):
            f = pkg_resources.resource_stream(__name__, fn_static)
            return leak_file(f)

        # Give up.
        return web.notfound()

def main():
    urls = ('/xspf', 'XSPF',
            '/', 'Index',
            '/(.*)', 'Static',)
    web.run(urls, globals())
