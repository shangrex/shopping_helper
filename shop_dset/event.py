import requests
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
import json

channel_access_token = getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

special_text = dict()

def same_msg(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

def entrance_msg(event, test_shop):
    init_node(event, test_shop)


def router_msg(event, node, test_shop):
    data = None
    end_check = False
    for i in test_shop:
        if node == i['id']:
            data = i
    if data['type'] == "end":
        end_check = True  
    for i in data['sections']:
        if i['type'] == "carousel":
            carousel_node(event, i)
        if i['type'] == 'text':
            text_node(event, i)
        if i['type'] == "img":
            image_node(event, i)
    
    if end_check == True:
        end_node(event, data)


def foward_special_text(event, test_shop):
    print(special_text)
    for i in special_text:
        if event.message.text in special_text:
            router_msg(event, special_text[event.message.text], test_shop)
            break

def init_node(event, test_shop):
    print("get into entrance")
    # print(test_shop[0]["sections"][2]["content"][0]['url'])

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


def carousel_node(event, data):
    image_object = []
    # print(data)
    for i in data["content"]:
        if i['buttons'] == None:
            # Case: None input
            button_txt = " "
            goto_state = " "
        elif i["buttons"][0]["edgeTo"] == "":
            button_txt = i['buttons'][0]["text"]
            goto_state = " "
        else:
            button_txt = i['buttons'][0]["text"]
            goto_state = i['buttons'][0]["edgeTo"]
        
        print("next state", goto_state)
        image_object.append(
            ImageCarouselColumn(
                image_url=i['url'],
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

def text_node(event, data):
    button_object = []
    if "buttons" in data:
        for i in data['buttons']:
            button_object.append(
                QuickReplyButton(action=MessageAction(label=i["text"], text=i["text"]))
            )
            special_text[i['text']] = i["edgeTo"]

            
    if len(button_object) != 0:
        text_message = TextSendMessage(
                            text=data["content"],
                            quick_reply=QuickReply(
                                items=button_object
                            )
                        )
    else:
        text_message = TextSendMessage(text=data["content"])
                

    line_bot_api.push_message(
        event.source.user_id,
        text_message    
    )


def image_node(event, data):    
    image_message = ImageSendMessage(
        original_content_url=data["url"],
        preview_image_url=data["url"]
    )
    line_bot_api.push_message(
        event.source.user_id,
        image_message    
    )


def end_node(event, data):
    # Example shop id
    shop_id = 1
    # s = "http://34.80.76.67:8000/shops/{0}".format(shop_id)
    # r = requests.get(s)
    # shop = json.loads(r.text)
    s = "http://34.80.76.67:8000/stat/relation"
    r = requests.get(s)
    track = json.loads(r.text)
    print(track)
    track_map = {}
    for i in range(30):
        track_map[str(i)] = 0
    for i in track:
        if i["visit_1"] == shop_id:
            track_map[str(i["visit_2"])] += 1

    track_map = dict(sorted(track_map.items(), key=lambda x:x[1], reverse=True))
    shop_object = []
    print(list(track_map.keys()))
    for i in range(5):
        recommed_id = list(track_map.keys())[i]
        print(recommed_id)
        if recommed_id == "0":
            continue
        s = "http://34.80.76.67:8000/shops/{0}".format(recommed_id)
        r = requests.get(s)
        shop = json.loads(r.text)
        print(shop)
        shop_object.append(
            CarouselColumn(
                thumbnail_image_url=shop["icon"],
                title=shop["name"],
                text=shop["description"]+"\n"+shop["category"]+"\n"+shop["phone_num"],
                actions=[
                    MessageAction(
                        label='Locaton',
                        text=shop["Location"]
                    ),
                    MessageAction(
                        label='Opening Hours',
                        text=shop["Opening Hours"]
                    ),
                    MessageAction(
                        label='People In Shop',
                        text=shop["People In Shop"]
                    ),
                ]
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=shop_object
        )
    )
    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text="其他您可能感興趣的店")
    )
    line_bot_api.push_message(
        event.source.user_id,
        carousel_template_message    
    )
