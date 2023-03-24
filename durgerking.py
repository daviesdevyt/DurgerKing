from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

bot = TeleBot("5998267047:AAFegC1eFwnk3eySSkxI8h6ZJ9C8IOA-1eM")

web_app = WebAppInfo(url="https://durger-king-five.vercel.app/")

order_inline_btn = InlineKeyboardButton("Order", web_app=web_app)

inline_markup = InlineKeyboardMarkup()
inline_markup.add(order_inline_btn)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome👋!\nI am a food delivery bot.\nWhat will you like to order today?",
                 reply_markup=inline_markup)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    send_welcome(message)

bot.infinity_polling()

