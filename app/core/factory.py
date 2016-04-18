#!/usr/bin/env python
#-*- coding: utf-8 -*-
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import reactor
from twisted.protocols.policies import TimeoutMixin
from twisted.python import log
from ..models import Client, collection
from . import common
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
clientlist = set()

import threading


def detection():
    log.msg(str(len(clientlist)))
    '''
    for item in clientlist:
        try:
            if item.transport.getTcpKeepAlive():
                item.transport.write(
                    'ret:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
                log.msg(str(item.transport.getTcpKeepAlive()) + ':' + item.transport.getPeer(
                ).host + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                item.factory.delClient(item, item.getId())
                log.msg('remove')
        except AttributeError:
            item.factory.delClient(item, item.getId())
            log.msg('remove attr')
    '''

def sayhello():
    global client
    print u'检查活跃主机：'+str(len(clientlist))
    '''
    for item in clientlist:
        try:
            if item.transport.getTcpKeepAlive():
                item.transport.write(
                    'ret:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
                print str(item.transport.getTcpKeepAlive()) + ':' + item.transport.getPeer().host + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            else:
                print 'diushi1'
        except AttributeError:
            print 'diushi2'
    '''
    global t  # Notice: use global variable!
    t=threading.Timer(5.0, sayhello)
    t.start()
t=threading.Timer(5.0, sayhello)
t.start()



class WXSH(LineOnlyReceiver):

    # def dataReceived(self, data):
    #    pass

    def lineReceived(self, line):
        # print 'line_' + line
        log.msg("Client connection from %s" % line)
        # self.factory.sendAll("%s" % (line))

    def getId(self):
        return str(self.transport.getPeer().host)

    def connectionMade(self):
        # print "New User Login: " + self.getId()
        # log.msg("New User Login: %s" % self.getId())
        try:
            self.transport.setTcpKeepAlive(1)
        except AttributeError:
            print 'close'
            log.msg("lose %s" % self.getId())
            self.factory.delClient(self, self.getId())

        self.factory.addClient(self, self.getId())
        self.transport.write("{'ret':1}")

    def connectionLost(self, reason):
        log.msg("close: %s" % self.getId())
        print self.getId() + 'close'
        self.factory.delClient(self, self.getId())

    def getlist(self):
        print 'start-------------'
        for item in self.clients:
            print str(item.transport.getTcpKeepAlive()) + ':' + item.transport.getPeer().host


class WXSHFactory(Factory,TimeoutMixin):
    protocol = WXSH

    global clientlist

    def __init__(self):
            # self.clients = []
        self.clients = set()
        self.player = []
        self.msg = ''
        self.x = range(100, 700)
        self.y = range(100, 500)
        log.msg('start')

    def getPlayerId(self):
        return len(self.player)

    def addClient(self, newclient, dev_id):

        # self.clients.append(newclient)
        clientlist.add(newclient)

        if Client.getcount(dev_id) == 0:
            c = Client()
            c._id = collection.get_next_id('client')
            c.user_id=1
            c._type=1
            c.device_id = dev_id
            c.state = 1
            c.save()
        else:
            Client.objects(device_id=dev_id).update_one(
                **{'set__state': 1, 'set__activa_data': common.getstamp()})

    def delClient(self, client, dev_id):
        # self.clients.discard(client)
        clientlist.remove(client)
        Client.objects(device_id=dev_id).update_one(
            **{'set__state': 0, 'set__activa_data': common.getstamp()})

    def sendAll(self, data):
        # print data
        if data.find('<policy-file-request/>') != -1:
            proto.transport.write(
                '<cross-domain-policy><allow-access-from domain="127.0.0.1" to-ports="*"/></cross-domain-policy>\0')
        else:
            arr = data.split(':')
            prefix = arr[0]
            content = arr[1]
            if prefix.find('player') != -1:
                newPlayer = [content, str(random.randrange(200, 600)), str(
                    random.randrange(150, 350)), str(random.randrange(1, 5))]
                self.player.append(newPlayer)
                self.msg = ' 玩家 ' + content + ' comments111!'
                # 广播所有玩家的位置
                temp = []
                playerData = ':::'
                for pos in self.player:
                    temp.append(string.join(pos, '---'))
                playerData = playerData + string.join(temp, '***')
                for proto in self.clients:
                    proto.transport.write('[系统]: ' + self.msg + '\n')
                    proto.transport.write(playerData)
            elif prefix.find('pos') != -1:
                playerName, x, y = content.split('---')
                i = 0
                for p in self.player:
                    if p[0] == playerName:
                        p[1] = x
                        p[2] = y
                for proto in self.clients:
                    proto.transport.write(data)
            else:
                self.msg = data
                for proto in self.clients:
                    proto.transport.write(self.msg + '\n')
