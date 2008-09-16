import moxie.web

def local(port = 8080):
    from wsgiref.simple_server import make_server
    server = make_server('', port, moxie.web.app())
    print 'http://localhost:%u/' % port
    server.serve_forever()
