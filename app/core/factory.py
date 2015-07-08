#!/usr/bin/env python
#-*- coding: utf-8 -*-
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import reactor
from twisted.python import log
from ..models import Client, collection
from . import common
import time

client = set()

import threading


def sayhello():
    global client
    print u'检查活跃主机：'
    i = 0
    for item in client:
        if i == 0:
            i += 1
            item.transport.write(
                'ret:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
        print str(item.transport.getTcpKeepAlive()) + ':' + item.transport.getPeer().host + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    global t  # Notice: use global variable!
    t = threading.Timer(5.0, sayhello)
    t.start()
t = threading.Timer(5.0, sayhello)
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
            print u'意外中断'
            log.msg("意外丢失 %s" % self.getId())
            self.factory.delClient(self, self.getId())

        self.factory.addClient(self, self.getId())
        self.transport.write("{'ret':1}")
        global client
        print client

    def connectionLost(self, reason):
        log.msg("已断开: %s" % self.getId())
        print self.getId() + u'已中断'
        self.factory.delClient(self, self.getId())

    def getlist(self):
        print 'start-------------'
        for item in self.clients:
            print str(item.transport.getTcpKeepAlive()) + ':' + item.transport.getPeer().host


class WXSHFactory(Factory):
    protocol = WXSH

    def __init__(self):
            # self.clients = []
        self.clients = set()
        self.player = []
        self.msg = ''
        self.x = range(100, 700)
        self.y = range(100, 500)
        print u'服务器已启动'

    def getPlayerId(self):
        return len(self.player)

    def addClient(self, newclient, dev_id):
        global client
        # self.clients.append(newclient)
        client.add(newclient)

        if Client.getcount(dev_id) == 0:
            c = Client()
            c._id = collection.get_next_id('client')
            c.device_id = dev_id
            c.state = 1
            c.save()
        else:
            Client.objects(device_id=dev_id).update_one(
                **{'set__state': 1, 'set__activa_data': common.getstamp()})

    def delClient(self, client, dev_id):
        # self.clients.remove(client)
        self.clients.discard(client)
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
