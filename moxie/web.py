import pkg_resources

import mako.lookup
import markdown
import selector
import webob

import moxie.music

class app(selector.Selector):
    templates = mako.lookup.TemplateLookup(directories = [pkg_resources.resource_filename(__name__, 'templates/')],
                                           filesystem_checks = True)
    index_template, xspf_template = map(templates.get_template, ('index.html', 'xspf.xml'))

    def __init__(self, directory = '.'):
        selector.Selector.__init__(self)

        self.music = moxie.music.Directory(directory)

        self.add('/', GET = self.index)
        #app.add('/xspf', GET = XSPF)
        #app.add('/{file}', GET = Static)

    index_template = templates.get_template('index.html')
    def index(self, environ, start_response):
        res = webob.Response()
        res.body = self.index_template.render(markdown = markdown.markdown,
                                              header = self.music.header,
                                              tracklist = self.music.tracks)
        return res(environ, start_response)

"""
def tracklist(url_root = ''):
    for count, fn in enumerate(files):
        info = TrackInfo(fn)
        url = urlparse.urljoin(url_root,
                               web.net.urlquote(web.http.url(fn)))

        yield count, info, url

#render = web.template.render(
#web.template.Template.globals['markdown'] = markdown.markdown


def cgi_tracklist():
    return tracklist(web.ctx.homedomain)

class XSPF:
    def GET(self):
        web.header('Content-Type', 'application/xspf+xml')
        print render.xspf(cgi_tracklist())

class Static:
    def leak_file(self, f):
        while True:
            buf = f.read(16 * 1024)
            if not buf:
                break
            yield buf
        f.close()

    def GET(self, filename):
        content_type, encoding = mimetypes.guess_type(filename)
        web.header('Content-Type', content_type)

        # Serve the music.
        if filename in files:
            return self.leak_file(file(filename))

        # Serve the necessities.
        fn_static = os.path.join('static', filename)

        if pkg_resources.resource_exists(__name__, fn_static):
            f = pkg_resources.resource_stream(__name__, fn_static)
            return self.leak_file(f)

        # Give up.
        return web.notfound()
"""
