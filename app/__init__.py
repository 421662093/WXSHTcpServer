#!/usr/bin/env python
#-*- coding: utf-8 -*-

# from config import config
from twisted.internet import protocol, reactor
from core import factory
from mongoengine import *
# Twisted Application Framework
# echo_server.tac
from twisted.application import internet, service
#import Pyro.core
from core import pyroserver
import time
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
db = connect('wxsh')

'''
def pyroserverThread():
        # 监听端口，创建守护线程
    daemon = Pyro.core.Daemon(host='localhost', port=9000)
    # 启动服务
    Pyro.core.initServer()
    # 创建代理对象
    proxy = Pyro.core.ObjBase()
    proxy.delegateTo(pyroserver.Echo())
    # 设置服务的名字为echo
    daemon.connect(proxy, "echo")
    # 循环调用给
    daemon.requestLoop()
'''


def create_app(config_name):
    pass
    #t = threading.Thread(target=pyroserverThread, name='pyroserverThread')
    # t.start()
    # t.join() #挂起主线程，等待子线程执行完毕
'''
def create_app(config_name):

    # reactor.listenTCP(8006, factory.WXSHFactory())
    application = service.Application("factory.WXSH")
    echoService = internet.TCPServer(8006, factory.WXSHFactory())
    echoService.setServiceParent(application)
    return echoService
'''
