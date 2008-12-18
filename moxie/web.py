import os.path

import mako.lookup
import selector
import static
import webob

import pkg_resources

import moxie.music

class uri(object):
    """A decorator for instance functions to attach a .uri_path and associate a template."""

    TEMPLATES = mako.lookup.TemplateLookup(directories = [pkg_resources.resource_filename(__name__, 'templates/')],
                                           filesystem_checks = True)

    def __init__(self, path, template):
        self.uri_path = path
        self.template = template

    def __call__(self, func):
        def replacement(instance, environ, start_response):
            req = webob.Request(environ)
            tmpl = self.TEMPLATES.get_template(self.template)

            resp = func(instance, req, tmpl, **req.urlvars)

            if isinstance(resp, basestring):
                resp = webob.Response(body = resp)
            elif isinstance(resp, dict):
                resp = webob.Response(**resp)

            return resp(environ, start_response)

        replacement.uri_path = self.uri_path

        return replacement

    @classmethod
    def uris(cls, instance):
        """Return the (uri, function) pairs on an instance class."""

        for name in dir(instance):
            func = getattr(instance, name)

            if hasattr(func, 'uri_path'):
                yield func.uri_path, func

class app(selector.Selector):
    """WSGI application for Moxie."""

    def __init__(self, directory = '.'):
        selector.Selector.__init__(self, consume_path = False, prefix = '/')

        self.music = moxie.music.TrackList(directory)

        # Register the dynamic URIs.
        for path, func in uri.uris(self):
            self.add(path, GET = func)

        # Register the static URIs.
        static_app = static.Cling(pkg_resources.resource_filename(__name__, 'static/'))

        for fn in pkg_resources.resource_listdir(__name__, 'static/'):
            self.add(fn, GET = static_app)

        # Register the music.
        music_app = static.Cling(directory)

        for fn in self.music:
            self.add(fn, GET = music_app)

        # Special-case for user CSS customizations.
        if os.path.exists(os.path.join(directory, 'local.css')):
            self.add('local.css', GET = music_app)

    @uri('', 'index.html')
    def index(self, request, template):
        return template.render(tracklist = self.music)

    @uri('xspf', 'xspf.xml')
    def xspf(self, request, template):
        return {'content_type': 'application/xspf+xml',
                'body': template.render(tracklist = self.music)}
 
    @uri('rss', 'rss.xml')
    def rss(self, request, template):
        return {'content_type': 'application/rss+xml',
                'body': template.render(tracklist = self.music,
                                        request = request)}		
