from wechat_sdk import WechatBasic
from wechat_public import app
from flask import request
from wechat_public.configure.settings import settings

@app.route('/')
def validate():
    wechat = WechatBasic(token=settings['wechat_app']['token'])
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    print "data:", signature, timestamp, nonce, request.args.get('echostr')
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return request.args.get('echostr')
    return ""
