# Twisted Application Framework
# server.tac
from app.models import Client
from app.core import factory
from twisted.application import internet, service
import os
from app import create_app

create_app(os.getenv('FLASK_CONFIG') or 'default')

application = service.Application("factory.WXSH")
echoService = internet.TCPServer(8006, factory.WXSHFactory())
echoService.setServiceParent(application)