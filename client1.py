#!/usr/bin/env python
#-*- coding: utf-8 -*-
from twisted.internet.protocol import ClientCreator, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys


class Sender(Protocol):

    def sendCommand(self, command):
        print "invio", command
        #self.transport.write(command + '\n')
        self.transport.getHandle().sendall(command + '\r\n' + 'sss\r\n___')

    def dataReceived(self, data):
        print data


PORT = 8006
HOST = '127.0.0.1'  # 182.254.221.13


def sendCommand(command):
    def test(d):
        print "Invio ->", command
        d.sendCommand(command)
    c = ClientCreator(reactor, Sender)
    c.connectTCP(HOST, PORT).addCallback(test)

if __name__ == '__main__':
    '''
    if len(sys.argv) != 2 or sys.argv[1] not in ['stop', 'next_call', 'force']:
        sys.stderr.write('Usage: %s: {stop|next_call|force}\n' % sys.argv[0])
        sys.exit(1)
    '''
    sendCommand('client' + '\n')  # sys.argv[1]
    reactor.run()
