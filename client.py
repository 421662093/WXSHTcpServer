#-*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from sys import stdout
import Pyro.core

PORT = 8006
HOST = '192.168.2.38'  # 182.254.221.13


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

'''
# 远程调用地址
url = 'PYROLOC://localhost:9000'
# 创建代理对象，返回的就是就是一个Echo对象的实例
proxy = Pyro.core.getProxyForURI(url + "/echo")
# 输出 Hello zhaolei
print proxy.say_hello("zhaolei")
# 输出Hello 石头
print proxy.say_hello("石头")
'''
reactor.connectTCP(HOST, PORT, EchoClientFactory())
reactor.run()
