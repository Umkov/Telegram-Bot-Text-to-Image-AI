import telebot
from config import SECRET, TOKEN, TELE_TOKEN
from logic import Text2ImageAPI



bot = telebot.TeleBot(TELE_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    # bot.reply_to(message, message.text)
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', SECRET, TOKEN)
    model_id = api.get_model()
    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)
    api.convert_image(images)
    with open('output.jpeg', 'rb') as processed_photo:
        bot.send_photo(message.chat.id, processed_photo)

bot.infinity_polling()