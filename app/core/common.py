# coding:utf-8

from flask import make_response
import json
import time
import cgi
import HTMLParser


# 自定义jsonify 解决flask.jsonify无法返回中文
def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(
        json.dumps(dict(**kwargs), ensure_ascii=False, indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


def stamp2time(stamp, _type='%Y-%m-%d %H:%M:%S'):  # 将时间戳转化为时间
        # time.gmtime(_time)
    return time.strftime(_type, time.localtime(stamp))


def time2stamp(_time, _type='%Y-%m-%d %H:%M:%S'):  # 将时间转化为时间戳

    return time.mktime(time.strptime(_time, _type))


def getstamp():  # 获取当前时间戳
    return time.time()


def getavatar(isa=1, userid=0, _type=1):  # 获取用户头像地址

    if isa == 1:
        return getavatar(userid, _type)
    else:
        if _type == 1:
            return "http://ava.fanka.me/noavatar_small.gif"
        elif _type == 2:
            return "http://ava.fanka.me/noavatar_middle.gif"
        else:
            return "http://ava.fanka.me/noavatar_big.gif"


def getavatar(userid=0, _type=1):  # 获取用户头像地址
    houzhui = ".jpg"
    avapath = "/data/avatar"

    # if _type > 0:
    # avapath = AvaImgDomain
    if _type == 1:
        houzhui = "_small.jpg"
    elif _type == 2:
        houzhui = "_middle.jpg"
    elif _type == 3 | _type == -1:
        houzhui = "_big.jpg"
    numbers = []
    userid = str(userid)

    for i in range(0, len(userid)):
        numbers.append(str(userid[i]))
    numlen = len(numbers)
    if numlen < 3:
        if numlen == 1:
            return avapath + "/000/00/00/0" + numbers[0] + houzhui
        else:
            return avapath + "/000/00/00/" + numbers[0] + numbers[1] + houzhui
    elif numlen < 5:
        if numlen == 3:
            return avapath + "/000/00/0" + numbers[0] + "/" + numbers[1] + numbers[2] + houzhui
        else:
            return avapath + "/000/00/" + numbers[0] + numbers[1] + "/" + numbers[2] + numbers[3] + houzhui
    elif numlen < 7:
        if numlen == 5:
            return avapath + "/000/0" + numbers[0] + "/" + numbers[1] + numbers[2] + "/" + numbers[3] + numbers[4] + houzhui
        else:
            return avapath + "/000/" + numbers[0] + numbers[1] + "/" + numbers[2] + numbers[3] + "/" + numbers[4] + numbers[5] + houzhui
    else:
        if numlen == 7:
            return avapath + "/00" + numbers[0] + "/" + numbers[1] + numbers[2] + "/" + numbers[3] + numbers[4] + "/" + numbers[5] + numbers[6] + houzhui
        elif numlen == 8:
            return avapath + "/0" + numbers[0] + numbers[1] + "/" + numbers[2] + numbers[3] + "/" + numbers[4] + numbers[5] + "/" + numbers[6] + numbers[7] + houzhui
        else:
            return avapath + "/" + numbers[0] + numbers[1] + numbers[2] + "/" + numbers[3] + numbers[4] + "/" + numbers[5] + numbers[6] + "/" + numbers[7] + numbers[8] + houzhui


def htmlescape(string):  # html编码
    return cgi.escape(string)


def htmlunescape(string):  # html反编码
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(string)
