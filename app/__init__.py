#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
#from config import config
from twisted.internet import protocol, reactor
from core import factory
from mongoengine import *
# Twisted Application Framework
# echo_server.tac
from twisted.application import internet, service

reload(sys)
sys.setdefaultencoding('utf-8')
db = connect('wxsh')


def create_app(config_name):
    pass
'''
def create_app(config_name):

    #reactor.listenTCP(8006, factory.WXSHFactory())
    application = service.Application("factory.WXSH")
    echoService = internet.TCPServer(8006, factory.WXSHFactory())
    echoService.setServiceParent(application)
    return echoService
'''
