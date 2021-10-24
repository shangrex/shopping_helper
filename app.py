from flask import Flask, request, jsonify, abort
from os import getenv
import json
from dotenv import load_dotenv
import requests
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
from shop_dset.event import entrance_msg, router_msg, foward_special_text

app = Flask(__name__)
load_dotenv()

channel_secret = getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
hwid = getenv("BEACON_ID", None)

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
    r""" Handle message event."""
    s = "http://34.80.76.67:8000/fsm/{0}".format(hwid)
    r = requests.get(s)
    shop = json.loads(r.text)
    shop = [json.loads(i["data"]) for i in shop]
    print(shop)
    foward_special_text(event, shop)


@handler.add(PostbackEvent)
def post_route(event):
    r"""Handle postback event."""
    print("post back event", event.postback.data)
    s = "http://34.80.76.67:8000/fsm/{0}".format(hwid)
    r = requests.get(s)
    shop = json.loads(r.text)
    shop = [json.loads(i["data"]) for i in shop]
    router_msg(event, event.postback.data, shop)    




@handler.add(BeaconEvent)
def handle_beacon_event(event):
    r"""Handle beacon event."""
    if event.beacon.hwid == "{your HWId}":
        msg = '{your message 1}'
    else:
        msg = 'you have received beacon.'
    s = "http://34.80.76.67:8000/fsm/{0}".format(hwid)
    r = requests.get(s)
    shop = json.loads(r.text)
    shop = [json.loads(i["data"]) for i in shop]
    print(shop)
    router_msg(event, "node_0", shop)


if __name__ == '__main__':
    port = getenv('PORT')
    app.run(host='0.0.0.0', port=port, debug=True)
