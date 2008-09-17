from __future__ import with_statement

import logging
import os
import shutil

from wsgiref.simple_server import make_server

import pkg_resources

import webob

import moxie.web

def local(bindaddr = '127.0.0.1', port = 8080):
    server = make_server(bindaddr, port, moxie.web.app())

    print 'http://%s:%u/' % (bindaddr, port)

    server.serve_forever()

def static():
    app = moxie.web.app()

    if not app.music:
        return logging.error('No music found.')

    # Dynamic files.
    for uri, func in moxie.web.uri.uris(app):
        req = webob.Request.blank('/' + uri)
        res = req.get_response(app)

        fn = uri if uri else 'index.html'

        with file(fn, 'w') as f:
            f.write(res.body)

    # Static files.
    for fn in pkg_resources.resource_listdir(__name__, 'static/'):
        with pkg_resources.resource_stream(__name__, os.path.join('static', fn)) as f_in:
            with file(fn, 'w') as f_out:
                shutil.copyfileobj(f_in, f_out)
