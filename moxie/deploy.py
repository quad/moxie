import moxie.web

def local(bindaddr = '127.0.0.1', port = 8080):
    from wsgiref.simple_server import make_server
    server = make_server(bindaddr, port, moxie.web.app())
    print 'http://%s:%u/' % (bindaddr, port)
    server.serve_forever()
