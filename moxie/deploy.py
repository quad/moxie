from __future__ import with_statement

import logging
import optparse
import os
import shutil
import urlparse
import webbrowser

from wsgiref.simple_server import make_server

import pkg_resources
import webob

import moxie.web

log = logging.getLogger(__name__)

def _setup_logging():
    _log_handler = logging.StreamHandler()
    _log_handler.setFormatter(logging.Formatter("%(message)s"))
    _log_handler.setLevel(logging.INFO)

    log.addHandler(_log_handler)

def local(bindaddr = 'localhost', port = 8080):
    """Deploy a test web server."""

    server = make_server(bindaddr, port, moxie.web.app())

    url = 'http://%s:%u/' % (bindaddr, port)

    print url
    webbrowser.open(url)

    server.serve_forever()

def static():
    """Deploy a set of static files to a directory."""

    # Parse the command-line.

    parser = optparse.OptionParser(usage='Usage: %prog [options] [directories ...]',
                                   description='Moxie Makes Mixtapes!')
    parser.add_option('-f', '--force', help='overwrite existing files', action='store_true')
    parser.add_option('-v', '--verbose', help='explain what is being done', action='store_true')
    parser.add_option('-u', '--url', help='the directory\'s base URL', action='store')
    (options, args) = parser.parse_args()

    # Set logging verbosity.

    _setup_logging()

    if options.verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARN)

    # Deploy to all specified directories. Use the current directory if none
    # were specified.

    if not args:
        args = ['.']
        log.info('Using current directory...')

    for d in args:
        app = moxie.web.app(d)

        if not app.music:
            log.error("Skipping %s (no music)" % d)
            continue

        # Generate the dynamic files.

        if not options.url:
            log.warn('No base URL specified (--url). Expect weirdness!')
            options.url = '/'

        for uri, func in moxie.web.uri.uris(app):
            req = webob.Request.blank(urlparse.urljoin(options.url, uri))
            res = req.get_response(app)

            fn = os.path.join(d, uri if uri else 'index.html')

            if os.path.exists(fn) and not options.force:
                log.warn("Skipping %s (file exists)" % fn)
            else:
                with file(fn, 'w') as f:
                    f.write(res.body)
                    log.info("Wrote %s" % fn)

        # Generate the static files.

        for bfn in pkg_resources.resource_listdir(__name__, 'static/'):
            with pkg_resources.resource_stream(__name__, os.path.join('static', bfn)) as f_in:
                fn = os.path.join(d, bfn)

                if os.path.exists(fn) and not options.force:
                    log.warn("Skipping %s (file exists)" % fn)
                else:
                    with file(fn, 'w') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                        log.info("Wrote %s" % fn)
