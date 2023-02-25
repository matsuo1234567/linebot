from flask import Flask, request, abort

from flask_cors import CORS

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
CORS(app)

line_bot_api = LineBotApi('Bv4GtyRVX3sgacDQQGdhtWHeiXroFKbpYnlsUjsiyV+lbXx8JVMGpoGu6i3X6J9rOLY9ryzCkRhYmg657nrDjM1XQfp3CPeSTxOVeTrvapBF0CtIIg9Ga29k0AxLNfo3P3swlIIpBUUeNm5jbSwYkAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('26e3312371b32adbed6917c01d932d28')

@app.route('/')
def a():
    return "hello world"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
