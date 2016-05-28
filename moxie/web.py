import contextlib
import os.path
import shutil
import tempfile
import urlparse
import wsgiref

import mako.lookup
import static
import webob

import pkg_resources

import moxie.music

class uri(object):
    """A decorator for instance functions to attach a .uri_path and associate a template."""

    TEMPLATES = mako.lookup.TemplateLookup(directories = [pkg_resources.resource_filename(__name__, 'templates')],
                                           filesystem_checks = True,
                                           default_filters = ['decode.utf8'],
                                           input_encoding = 'utf-8',
                                           output_encoding = 'utf-8')

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

TEMPLATES = {
        'index.html': 'index.html',
        'index.xspf': 'xspf.xml',
        'index.rss': 'rss.xml',
}

class FakeRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def relative_url(self, relative_url):
        return urlparse.urljoin(self.base_url, relative_url)

def deploy(base_url, source_directory, target_directory):
    tracklist = moxie.music.TrackList(source_directory)

    # Templates
    for output_filename, template_name in TEMPLATES.iteritems():
        with file(os.path.join(target_directory, output_filename), 'w') as f:
            body = uri.TEMPLATES.get_template(template_name).render(
                    tracklist = tracklist,
                    request = FakeRequest(base_url))
            f.write(body)

    # Static
    static_directory = pkg_resources.resource_filename(__name__, 'static')

    for fn in pkg_resources.resource_listdir(__name__, 'static'):
        shutil.copy(os.path.join(static_directory, fn), target_directory)

    # Music
    for fn in tracklist:
        shutil.copy(os.path.join(source_directory, fn), target_directory)

    # User CSS
    if os.path.exists(os.path.join(source_directory, 'local.css')):
        shutil.copy(os.path.join(source_directory, 'local.css'), target_directory)

@contextlib.contextmanager
def tempdir():
    dn = tempfile.mkdtemp()
    try:
        yield dn
    finally:
        shutil.rmtree(dn)

class app:
    """WSGI application for Moxie."""

    def __init__(self, directory = '.'):
        self.directory = directory
        self.music = moxie.music.TrackList(directory)

    def __call__(self, environ, start_response):
        with tempdir() as temporary_directory:
            base_url = wsgiref.util.application_uri(environ)
            deploy(base_url, self.directory, temporary_directory)

            static_app = static.Cling(temporary_directory)
            return static_app(environ, start_response)

    @uri('', 'index.html')
    def index(self, request, template):
        return template.render(tracklist = self.music)

    @uri('index.xspf', 'xspf.xml')
    def xspf(self, request, template):
        return {'content_type': 'application/xspf+xml',
                'body': template.render(tracklist = self.music)}

    @uri('index.rss', 'rss.xml')
    def rss(self, request, template):
        return {'content_type': 'application/rss+xml',
                'body': template.render(tracklist = self.music,
                                        request = request)}
