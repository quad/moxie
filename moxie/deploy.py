from __future__ import with_statement

import logging
import optparse
import os
import shutil

from wsgiref.simple_server import make_server

import pkg_resources
import webob

import moxie.web

def local(bindaddr = '127.0.0.1', port = 8080):
    """Deploy a test web server."""

    server = make_server(bindaddr, port, moxie.web.app())

    print 'http://%s:%u/' % (bindaddr, port)

    server.serve_forever()

def static():
    """Deploy a set of static files to a directory."""

    # Parse the command-line.

    parser = optparse.OptionParser()
    parser.add_option('-f', '--force', help='overwrite existing files', action='store_true')
    (options, args) = parser.parse_args()

    # Look for the music!

    app = moxie.web.app()

    if not app.music:
        return logging.fatal('No music found.')

    # Generate the dynamic files.

    for uri, func in moxie.web.uri.uris(app):
        req = webob.Request.blank('/' + uri)
        res = req.get_response(app)

        fn = uri if uri else 'index.html'

        if os.path.exists(fn) and not options.force:
            logging.warn("Skipping %s (file exists)" % fn)
        else:
            with file(fn, 'w') as f:
                f.write(res.body)

    # Generate the static files.
    for fn in pkg_resources.resource_listdir(__name__, 'static/'):
        with pkg_resources.resource_stream(__name__, os.path.join('static', fn)) as f_in:
            if os.path.exists(fn) and not options.force:
                logging.warn("Skipping %s (file exists)" % fn)
            else:
                with file(fn, 'w') as f_out:
                    shutil.copyfileobj(f_in, f_out)
