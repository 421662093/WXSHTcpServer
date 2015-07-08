#-*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from sys import stdout

PORT = 8006
HOST = '127.0.0.1'  # 182.254.221.13


class Echo(Protocol):

    def dataReceived(self, data):
        print data
        # stdout.write(data)

    def sendCommand(self, command):
        print "invio", command
        #self.transport.write(command + '\n')
        self.transport.getHandle().sendall(command + '\r\n' + 'sss\r\n___')


class EchoClientFactory(ClientFactory):

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Echo()

    def clientConnectionLost(self, connector, reason):
        connector.connect()
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

reactor.connectTCP(HOST, PORT, EchoClientFactory())
reactor.run()
