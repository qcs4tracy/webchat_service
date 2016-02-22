from wechat_sdk import WechatBasic
from wechat_public import app
from flask import request
from wechat_public.configure.settings import settings
from wechat_public.logging.log import logger

@app.route('/')
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


@app.route('/receive', methods=['POST'])
def receive():
    wechat = WechatBasic(token=settings['wechat_app']['token'], appid=settings['wechat_app']['appID'],
                     appsecret=settings['wechat_app']['appsecret'])
    wechat.parse_data(request.get_data(as_text=True))
    message = wechat.get_message()
    print (dir(message))
    return ""