#!/usr/bin/env python

import glob
import os.path
import sys
import xml.etree.ElementTree as ET
import urlparse

import web
import mutagen
import mutagen.id3
import mutagen.easyid3

path = 'static/'

files = sorted(glob.glob(os.path.join(path, '*.mp3')))
render = web.template.render('templates/')

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
        url = urlparse.urljoin(web.ctx.homedomain, web.net.urlquote(web.http.url(fn)))

        yield count, info, url

class XSPF:
    def GET(self):
        web.header('Content-Type', 'application/xspf+xml')
        print render.xspf(tracklist())

class Index:
    def GET(self):
        xspf_url = urlparse.urljoin(web.ctx.homedomain, '/xspf')
        print render.index(xspf_url, tracklist())

if __name__ == '__main__':
    urls = ('/xspf', 'XSPF',
            '/', 'Index',)
    web.run(urls, locals())
