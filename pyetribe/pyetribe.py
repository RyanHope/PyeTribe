# -*- coding:	utf-8 -*-
#===============================================================================
# This file is part of PyeTribe.
# Copyright (C) 2015 Ryan Hope <rmh3093@gmail.com>
#
# PyViewX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyViewX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyViewX.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall

from panglery import Pangler

import json

class EyeTribeClient(LineReceiver):
    
    delimiter = "\n"
    
    def _send_heartbeat(self):
        self.transport.write(json.dumps({"category":"heartbeat"}))        
    
    def connectionMade(self):
        self.heartbeat = LoopingCall(self._send_heartbeat)
        self.transport.write(json.dumps({"category":"tracker","request":"get","values":["heartbeatinterval"]}))
        self.transport.write(json.dumps({"category":"tracker","request":"set","values":{"push":True}}))
        
    def connectionLost(self):
        if self.heartbeat.running:
            self.heartbeat.stop()

    def lineReceived(self, line):
        response = json.loads(line)
        print response
        if response["category"] == "tracker" and response.has_key("values"):
            for val in response['values']:
                if val == "heartbeatinterval":
                    if self.heartbeat.running:
                        self.heartbeat.stop()
                    self.heartbeat.start(response['values'][val]/1000.0)
                    

class EyeTribeClientFactory(ClientFactory):
    
    protocol = EyeTribeClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

if __name__ == '__main__':
    factory = EyeTribeClientFactory()
    reactor.connectTCP('192.168.0.17', 6555, factory)
    reactor.run()