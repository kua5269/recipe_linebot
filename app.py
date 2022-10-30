from __future__ import unicode_literals

import configparser
import random

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (CarouselColumn, CarouselTemplate, ImageSendMessage,
                            MessageAction, MessageEvent, StickerSendMessage,
                            TemplateSendMessage, TextMessage, TextSendMessage)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# LINE get API

def get_image_message():
    img_message = ImageSendMessage(
        original_content_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Chateaubriand_roast.jpg/800px-Chateaubriand_roast.jpg',
        preview_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Chateaubriand_roast.jpg/800px-Chateaubriand_roast.jpg'
    )
    return img_message


def get_text_message():
    text_message = TextSendMessage(text='牛排套餐')
    return text_message


def get_carousel_template():
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Taiwanese_cuisine.jpg/1920px-Taiwanese_cuisine.jpg',
                    title='台式料理',
                    text='路邊小吃、辦桌大菜...',
                    actions=[
                        MessageAction(
                            label='來個台式',
                            text='台式料理'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/57/Oseti.jpg',
                    title='日式料理',
                    text='定食、壽司...',
                    actions=[
                        MessageAction(
                            label='來個日式',
                            text='日式料理'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/59/Spaghetti_vongole_2.jpg',
                    title='義式料理',
                    text='冷湯、比薩、燉飯...',
                    actions=[
                        MessageAction(
                            label='來個義式',
                            text='義式料理'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/53/Pho-Beef-Noodles-2008.jpg',
                    title='越式料理',
                    text='河粉、炸春捲...',
                    actions=[
                        MessageAction(
                            label='來個越式',
                            text='越式料理'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/2019.01.18_LCHF_Food%2C_Washington%2C_DC_USA_09714_%2846102636824%29.jpg/1024px-2019.01.18_LCHF_Food%2C_Washington%2C_DC_USA_09714_%2846102636824%29.jpg',
                    title='美式料理',
                    text='漢堡、牛排...',
                    actions=[
                        MessageAction(
                            label='來個美式',
                            text='美式料理'
                        )
                    ]
                )
            ]
        )
    )
    return carousel_template_message


def get_sticker_message():
    sticker_message = StickerSendMessage(
        package_id='789',
        sticker_id='10865'
    )
    return sticker_message


# 接收 LINE 的資訊
@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 不想動腦 -> Image message + Text message
    if event.message.text == '不想動腦':

        # 參考 -> https://github.com/line/line-bot-sdk-python/issues/67
        reply_obj = [
            get_image_message(),
            get_text_message()
        ]

    # 自選某式 -> Template message：Carousel template
    elif event.message.text == '自選某式':
        reply_obj = get_carousel_template()

    # 選購食材 -> Sticker message
    elif event.message.text == '添購食材':
        reply_obj = get_sticker_message()

    # 學你說話 + 彩色愛心
    else:
        pretty_note = '❤🧡💛💚💙💜🤎🖤🤍'
        pretty_text = ''

        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)
            reply_obj = TextSendMessage(text=pretty_text)

    line_bot_api.reply_message(
        event.reply_token,
        reply_obj
    )


if __name__ == "__main__":
    app.debug = True
    app.run()
