from flask import Flask, request, jsonify, abort
from os import getenv
from dotenv import load_dotenv
import datetime as dt
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, BeaconEvent,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, URIAction, TemplateSendMessage, PostbackEvent
)

from shop_dset.test_set import test_shop
from shop_dset.event import entrance_msg

app = Flask(__name__)
load_dotenv()

channel_secret = getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
# parser = WebhookParser(channel_secret)




@app.route('/', methods=['GET', 'POST'])
def test():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'ok'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    entrance_msg(event, 0)


@handler.add(PostbackEvent)
def post_route(event):
    print("post back event")
    print(event.postback.data)
    if event.postback.data == "node_3":
        entrance_msg(event, 3)    
    if event.postback.data == "node_4":
        entrance_msg(event, 4)


@handler.add(BeaconEvent)
def handle_beacon_event(event):
    if event.beacon.hwid == "{your HWId}":
        msg = '{your message 1}'
    else:
        msg = 'you have received beacon.'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )

if __name__ == '__main__':
    port = getenv('PORT')
    app.run(host='0.0.0.0', port=port, debug=True)
