from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from twisted.internet import reactor
from twisted.python import log
from peerlyDB.network import Server
import sys, signal
import json


class P2PNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_bootstrap(self, ipport):
        if (self.request['bootstraped']):
            log.msg('bootsrap is already done')
            self.emit('connected to network')
            return
        log.msg('starting bootstrap')
        (ip,port) = ipport.split(':')
        #server.bootstrap([("127.0.0.1", 8468)]).addCallback(P2PNamespace.sbootstrapDone, self)
        self.request['kadServer'].bootstrap([(ip, int(port))]).addCallback(self.bootstrapDone)

        self.emit('connecting to network')

    def recv_disconnect(self):
        self.disconnect(silent=True)

    def recv_message(self, message):
        pass
        #print "PING!!!", message
    
    def bootstrapDone(self,found):
        self.request['bootstraped'] = True
        log.msg('bootstrap done!!')
        self.emit('connected to network')

        
    def on_query(self, message):
        log.msg('query recieved '+message)
        keywords = message.split(' ')
        if (self.request['kadServer'] is None):
           return
        num = min(len(keywords),16)
        for i in range(0,num):
            self.request['kadServer'].get(keywords[i]).addCallback(self.queryDone,message)
            
    def queryDone(self, result, query):
        if(result is None):
            result = 'null'
        log.msg('query done '+str(result))
        self.emit('query result', result)
        
    def on_insert(self, m):
        if (self.request['kadServer'] is None):
            self.emit('insert result', 'Error: Cannot reach p2p network')
            return
        log.msg('insert '+ str(m))
        if (not isinstance(m, dict)) or  not ('url' in m and 'title' in m and 'keywords' in m):
            log.msg('Not a dictionary or invalid stoping...')
            self.emit('insert result','Error: Invalid object')
            return
        keywords = m.get('keywords').split(' ')
        num = min(len(keywords),16)
        for i in range(0,num):
            self.request['kadServer'].set(keywords[i], json.dumps(m)).addCallback(self.insertDone)
            
    def insertDone(self,result):
        if result is None:
          log.msg('insert error')
        else:
          log.msg('insert done '+str(result))
        self.emit('insert result', result)
     
    def on_my_ip(self):
        log.msg("asking my ip")
        ip = self.request['kadServer'].inetVisibleIP().addCallback(self.myIpDone)

    def myIpDone(self,ip):
        log.msg("my ip is %s" % (ip))
        self.emit('your ip', ip)
