from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, BeaconEvent,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, URIAction, TemplateSendMessage,
    ImageCarouselColumn, ImageCarouselTemplate, ImageSendMessage,
    QuickReply, QuickReplyButton
)
from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from os import getenv
from dotenv import load_dotenv
from shop_dset.test_set import test_shop


channel_access_token = getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

def same_msg(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

def entrance_msg(event, node):
    if node == 0:
        init_node(event)
    if node == 3:
        third_node(event)
    if node == 4:
        forth_node(event)


def init_node(event):
    print("get into entrance")
    # print(test_shop[0]["sections"][2]["content"][0]['url'])
    image_message = ImageSendMessage(
        original_content_url=test_shop[0]["sections"][0]["url"],
        preview_image_url=test_shop[0]["sections"][0]["url"]
    )
    text_message = TextSendMessage(text=test_shop[0]["sections"][1]["content"],
                        quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="Location", text="A1-3"))
                        ,QuickReplyButton(action=MessageAction(label="About Us", text="We are familey."))
                        ])
                    )

    # Fill image_carousel data
    image_object = []
    for i in range(len(test_shop[0]["sections"][2]["content"])):
        if test_shop[0]["sections"][2]["content"][i]['buttons'] == None:
            button_txt = " "
            goto_state = " "
        else:
            button_txt = test_shop[0]["sections"][2]["content"][i]['buttons']["text"]
            goto_state = test_shop[0]["sections"][2]["content"][i]['buttons']["edgeTo"]
        
        image_object.append(
            ImageCarouselColumn(
                image_url=test_shop[0]["sections"][2]["content"][i]['url'],
                action=PostbackAction(
                    label=button_txt,
                    display_text=button_txt,
                    data=goto_state
                )
            )
        )
    
    image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns=image_object
        )
    )


    line_bot_api.push_message(
        event.source.user_id,
        image_carousel_template_message
    )
    line_bot_api.push_message(
        event.source.user_id,
        text_message
    )


def third_node(event):
    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text="welcome to third node.")
    )

def forth_node(event):
    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text="welcome to forth node.")
    )