#!/usr/bin/env python
#-*- coding: utf-8 -*-
from mongoengine import *
from core import common


class Permission:
    USER = 0x01
    LIST_USER = 0x11
    EDIT_USER = 0x12
    DISCOVERY = 0x02
    INDEX_DISCOVERY = 0x21
    ADMINISTER = 0x80


class collection(Document):
    meta = {
        'collection': 'collection',
    }
    name = StringField(max_length=30, required=True)
    index = IntField(required=True)

    @staticmethod
    def get_next_id(tablename):
        doc = collection.objects(name=tablename).modify(inc__index=1)
        if doc:
            return doc.index + 1
        else:
            collection(name=tablename, index=1).save()
            return 1


class Client(Document):  # 客户端
    __tablename__ = 'client'
    meta = {
        'collection': __tablename__,
    }
    _id = IntField(primary_key=True)
    device_id = StringField(
        default='', max_length=64, required=True, db_field='di')
    activa_data = IntField(default=common.getstamp(), db_field='ad')  # 最后活动时间
    state = IntField(default=0, db_field='s')  # 状态

    @staticmethod
    def getcount(devid):
        return Client.objects(device_id=devid).count()
