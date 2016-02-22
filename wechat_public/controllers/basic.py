# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from wechat_public import app
from flask import request
from wechat_public.configure.settings import settings
from wechat_public.logging.log import logger
import zmq
import re

def track_validator(rule):
    def register(f):
        f.rule = rule
        f.matcher = re.compile(f.rule)
        return f

    return register


class TrackingNoValidtorBase(object):
    def check(self, data):
        x = self.extract(data)
        return len(x) > 0

    def extract(self, data):
        return self.matcher.findall(data)


@track_validator(u'GA[0-9]{9}US')
class TrackingNoValidator(TrackingNoValidtorBase):
    def __init__(self):
        pass

validator = TrackingNoValidator()

@app.route('/ignore')
def validate():
    wechat = WechatBasic(token=settings['wechat_app']['token'], appid=settings['wechat_app']['appID'],
                         appsecret=settings['wechat_app']['appsecret'])
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    # log the checking event
    logger.info("checking signature: (%s, %s, %s)", signature, timestamp, nonce)
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return request.args.get('echostr')
    return ""


HELP_MESSAGE = u'输入的单号不正确.(正确的单号格式: GA[9位数字]US, 比如: GA207886955US.)'
from track_data import TrackData

def check_status(data):
    return data['status'] != 0

STATUS_MAP = {0: u"您查询的单号还没有跟踪信息.", 1: u"最新的追踪信息:\n"}
TRACK_INFO_TMP = u'到{time}为止的最新追踪信息:\n\t{track_info}.[{track_time}]'
def status_message(status):
    return STATUS_MAP.get(status, "")

db = TrackData()
zmq_conf = settings['zmq']
_context = zmq.Context()
push_sock = zmq.socket(zmq.PUSH)
push_sock.connect('%s:%d' % (zmq['domain'], zmq['port']))

@app.route('/', methods=['POST'])
def receive():
    wechat = WechatBasic(token=settings['wechat_app']['token'], appid=settings['wechat_app']['appID'],
                         appsecret=settings['wechat_app']['appsecret'])
    data = request.get_data(as_text=True)
    for k, v in request.headers:
        print '%s : %s' % (k, v)
    print data
    wechat.parse_data(data)
    message = wechat.get_message()
    if message.type == 'text':
        content = message.content
        res = validator.extract(content)
        if not res:
            return wechat.response_text(HELP_MESSAGE)
        # has track no in the text message
        isadding = content.startswith(u'ZQQ')
        if isadding:
            for track_no in res:
                push_sock.send(u'{"track_no": %s}' % track_no)
            response = wechat.response_text(u'%s\n已添加.' % (u'\n'.join(res),))
        else:
            track_no = res[0]
            record = db.find_one(track_no)
            if record['status'] == 0:
                return wechat.response_text(status_message(record['status']))
            # has track data for this track No.
            latest = record['data'][-1]
            track = latest['location'] + ', ' + latest['context']
            track_time = latest['time']
            response = wechat.response_text(TRACK_INFO_TMP.format(time=record['time'], track_info=track,
                                                                  track_time=track_time))
        return response
    else:
        return wechat.response_text(u'对不起,目前不支持非文本消息~ ^_^')

    return 'success'
