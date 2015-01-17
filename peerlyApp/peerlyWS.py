from gevent import monkey; monkey.patch_all()

import gevent

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from twisted.internet import reactor, task, defer
from twisted.python import log
from peerlyDB.network import Server
import sys, signal

from p2p import P2PNamespace

log.startLogging(sys.stdout)


class Application(object):
    def __init__(self, port=8469):
        self.buffer = []
        # Dummy request object to maintain state between Namespace
        # initialization.
        server = Server()
        server.listen(port)
        
        self.request = {
            'queries': {},
            'kadServer' : server,
            'inserts' : {},
            'port' : port,
            'bootstraped' : False
        }
        
        gevent.spawn(self.startReactor) 

    def startReactor(self):
        gevent.sleep(1)
        reactor.run()
        signal.signal(signal.SIGINT, signal.default_int_handler)

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')
        if not path:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [open('peerlyApp/web/peerly.html').read()]
            #return ['<h1>Welcome. '
            #    'Try the <a href="/chat.html">chat</a> example.</h1>']

        if path.startswith('static/') or path == 'peerly.html':
            try:
                data = open('peerlyApp/web/'+path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'': P2PNamespace}, self.request)
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


      




