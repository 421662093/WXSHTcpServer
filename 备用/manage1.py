#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

from app import create_app
#from app.models import User, Follow, Role, Permission, Post, Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()
