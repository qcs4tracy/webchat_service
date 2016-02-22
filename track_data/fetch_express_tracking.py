# -*- coding: utf-8 -*-
import urllib
import urllib2
import random
import json

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'BAEID=7CD4EBC528C40A69A7D8EF33E66B22EC:FG=1; _gat=1; _ga=GA1.2.2111438798.1456116497',
    'Host': 'www.ckd8.com',
    'Origin': 'http://www.ckd8.com',
    'User-Agent': 'runscope/0.1,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

_decoder = json.JSONDecoder()

URL_TEMPLATE = 'http://www.ckd8.com/open.php?tmp=%s'

# data: [{time: 1454342400, context: "货物进入操作中心", location: "美国飞洋仓库"},…]
# from: "洛杉矶"
# message: ""
# name: ""
# packages: "1"
# size: ""
# state: "3"
# status: "1"
# time: 1456162577
# to: "中国"
# usetime: {day: 19, hour: 13, minute: 1}
# weight: ""
# Name

import datetime


def make_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime(u'%Y-%m-%d %H:%M')


def fetch_tracking_data(trackno):
    trackno = unicode(trackno)
    tmp = random.random()
    url = URL_TEMPLATE % (str(tmp),)
    values = {'com': 'feiyang', 'nu': '', 'tp': '2', 'wd': trackno}

    # com=feiyang&wd=GA207886955US&nu=&tp=2
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)

    try:
        data = _decoder.decode(response.read())
    except ValueError:
        data = {}

    COPY_FIELDS = ['from', 'to', 'data', 'packages', 'state', 'usetime']
    track_data = {}

    track_data['track_no'] = trackno
    track_data['time'] = make_time(data['time'])

    if track_data['status'] == '0':
        track_data['status'] = 0
    else:
        track_data['status'] = 1
        for field in COPY_FIELDS:
            track_data[field] = data[field]

    return track_data


STATUS_MAP = {0: u"您查询的单号还没有跟踪信息.", 1: u"最新的追踪信息:\n"}


def check_status(data):
    return data['status'] != 0
