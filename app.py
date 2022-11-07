from __future__ import unicode_literals

import configparser
import random

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (CarouselColumn, CarouselTemplate, ImageSendMessage,
                            MessageAction, MessageEvent, StickerSendMessage,
                            TemplateSendMessage, TextMessage, TextSendMessage,
                            QuickReply, QuickReplyButton)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 食譜們
recipes = [
    {
        "id": "0",
        "name": "❤蝦仁茶碗蒸",
        "type": "JP",
        "img": "https://www.kikkoman.com.tw/tmp/image/20131202/20131202224548_60470.jpg"
    },
    {
        "id": "1",
        "name": "❤起司漢堡排咖哩飯",
        "type": "JP",
        "img": "https://media.vogue.com.tw/photos/5fb5e0219f4703cad30e631d/master/w_1600,c_limit/%E6%A9%AB%E5%9C%96-%E8%B5%B7%E5%8F%B8%E6%BC%A2%E5%A0%A1%E6%8E%92%E5%92%96%E5%93%A9%E9%A3%AF.jpg"
    },
    {
        "id": "2",
        "name": "❤蘆筍青醬義大利麵",
        "type": "IL",
        "img": "https://www.simplyrecipes.com/thmb/KkXbfzRh5CEh-p1Abm6BTo4Grn0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2009__04__asparagus-pesto-pasta-horiz-a-1600-c9b6f4ba4fc4429391a5548847c6e724.jpg"
    },
    {
        "id": "3",
        "name": "❤古早味炒米粉",
        "type": "TW",
        "img": "https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2021/08/05/draft/13199669.jpeg&x=0&y=0&sw=0&sh=0&w=1050&h=800&exp=3600"
    },
    {
        "id": "4",
        "name": "番茄牛肉河粉",
        "type": "VT",
        "img": "https://cdn.walkerland.com.tw/images/upload/poi/p79087/m31597/ee901d5aa9bbe7eeac5eb327abf9b102de0e1bf3.jpg"
    },
    {
        "id": "5",
        "name": "❤烤豬肋排",
        "type": "US",
        "img": "https://tokyo-kitchen.icook.network/uploads/recipe/cover/406128/e3216f16acee29f5.jpg"
    },
    {
        "id": "6",
        "name": "❤味噌燒鯖魚",
        "type": "JP",
        "img": "https://shun-gate.com/wp-content/uploads/2021/12/sabamiso-1568x1045.jpg"
    },
    {
        "id": "7",
        "name": "❤奶油蘑/洋菇燉飯",
        "type": "IL",
        "img": "https://pic.pimg.tw/pinlegu2013/1470729588-650241142.jpg"
    },
    {
        "id": "8",
        "name": "❤沙卡蔬卡（北非蛋）",
        "type": "IL",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Shakshuka_by_Calliopejen1.jpg/1024px-Shakshuka_by_Calliopejen1.jpg"
    }
]


# 食譜照樣式分類
def type_of_cuisines(cuisine):

    return type_of_cuisines

# LINE get APIs
def get_image_message(img):
    img_message = ImageSendMessage(
        original_content_url=img,
        preview_image_url=img
    )
    return img_message


def get_text_message(recipe):
    text_message = TextSendMessage(recipe)
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
                            text='@台式料理'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/57/Oseti.jpg',
                    title='日式料理',
                    text='定食、壽司、拉麵...',
                    actions=[
                        MessageAction(
                            label='來個日式',
                            text='@日式料理'
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
                            text='@義式料理'
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
                            text='@越式料理'
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
                            text='@美式料理'
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

    if event.message.text[0] == '*':
        # reply_obj = TextSendMessage('顯示出圖文選單囉')

        # 不想動腦 -> Image message + Text message
        if event.message.text.find('不想動腦') != -1:
            ran_num = random.randint(0, 8)
            recipe = recipes[ran_num]
            # 參考 -> https://github.com/line/line-bot-sdk-python/issues/67
            reply_obj = [
                get_image_message(recipe["img"]),
                get_text_message(recipe["name"])
            ]

        # 自選某式 -> Template message：Carousel template
        elif event.message.text.find('自選某式') != -1:
            reply_obj = get_carousel_template()

        # 選購食材 -> Sticker message +
        elif event.message.text.find('添購食材') != -1:
            url = 'https://shop.pxmart.com.tw/page/justahour'
            url_text = '全聯小時達馬上為您送達: '+url
            reply_obj = [
                get_sticker_message(),
                TextSendMessage(text=url_text)
            ]

        else:
            unknown_text = '您輸入的是什麼美食呀？\n真抱歉我不認識這道菜耶。\n歡迎從左下方 ≡ 選單，\n點入找食譜來做菜囉！'
            reply_obj = TextSendMessage(text=unknown_text)

    elif event.message.text[0] == '@':
        # reply_obj = TextSendMessage('顯示出某式料理')

        if event.message.text.find('台式料理') != -1:
            items_tw =
            reply_obj = TextSendMessage(text='請選擇！想要吃哪個台：',
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(
                                                label="label1", text="name1")),
                                            QuickReplyButton(action=MessageAction(
                                                label="label2", text="name2")),
                                        ],))
            # reply_obj = [
            #     get_image_message(),
            #     get_text_message()
            # ]
        elif event.message.text.find('日式料理') != -1:
            reply_obj = TextSendMessage('日')
        elif event.message.text.find('義式料理') != -1:
            reply_obj = TextSendMessage('義')
        elif event.message.text.find('越式料理') != -1:
            reply_obj = TextSendMessage('越')
        elif event.message.text.find('美式料理') != -1:
            reply_obj = TextSendMessage('美')
        else:
            unknown_text = '您輸入的是什麼美食呀？\n真抱歉我不認識這道菜耶。\n歡迎從左下方 ≡ 選單，\n點入找食譜來做菜囉！'
            reply_obj = TextSendMessage(text=unknown_text)

    else:    # 學舌噴心鸚鵡 -> 提示輸入正確資訊
        # pretty_note = '❤🧡💛💚💙💜🤎🖤🤍'
        # pretty_text = ''
        # for i in event.message.text:
        #     pretty_text += i
        #     pretty_text += random.choice(pretty_note)
        #     reply_obj = TextSendMessage(text=pretty_text)
        unknown_text = '您輸入的是什麼美食呀？\n真抱歉我不認識這道菜耶。\n歡迎從左下方 ≡ 選單，\n點入找食譜來做菜囉！'
        reply_obj = TextSendMessage(text=unknown_text)

    line_bot_api.reply_message(
        event.reply_token,
        reply_obj
    )


if __name__ == "__main__":
    app.debug = True
    app.run()
