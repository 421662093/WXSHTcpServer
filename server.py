#-*- coding: utf-8 -*-
# Twisted Application Framework
# server.tac
from twisted.internet import reactor
from app.models import Client
from app.core import factory
import os
from app import create_app

create_app(os.getenv('FLASK_CONFIG') or 'default')

reactor.listenTCP(8006, factory.WXSHFactory())
reactor.protocol = factory.WXSH
#reactor.callLater(10, factory.detection)
reactor.run()
