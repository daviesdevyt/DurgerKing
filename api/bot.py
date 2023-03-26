from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from .tgkeyboards import *
from .models import User
from .index import db

bot = TeleBot("5998267047:AAFegC1eFwnk3eySSkxI8h6ZJ9C8IOA-1eM")
owner = 1289366093
send_messaage_mode = []

@bot.message_handler(commands=['help', 'start'])
def start(message: Message):
    bot.reply_to(message, "Welcome to adbot",
                 reply_markup=start_inline_markup(message.chat.id))

@bot.callback_query_handler(func=lambda call: call.data != None)
def account(callback: CallbackQuery):
    if callback.data == "home":
        start(callback.message)
        return
    
    if callback.data == "support":
        bot.edit_message_text("Contact for more info", callback.message.chat.id, callback.message.message_id, reply_markup=back_btn("home"))
        return

    if callback.data == "account":
        callback.message.chat
        if not User.query.get(callback.message.chat.id):
            bot.send_message(callback.message.chat.id, "You have no active subscription. Use /order to choose a subscription")
            return
        bot.send_message(callback.message.chat.id, f"Hello {callback.chat.username}.\nWhat do you want to do tody?", reply_markup=account_markup)

    if callback.data == "edit_message":
        edit_message(callback.message)

@bot.message_handler(commands=["editmessage"])
def edit_message(message: Message):
    send_messaage_mode.append(message.chat.id)
    bot.send_message(message.chat.id, "Send the new message you want to set")

@bot.message_handler(func=lambda message: True)
def echo_message(message: Message):
    if message.chat.id in send_messaage_mode:
        send_messaage_mode.remove(message.chat.id)
        User.query.get(message.chat.id).message = message.text
        db.session.commit()
        bot.reply_to(message, f"Message updated !! to {message.text}")
        bot.send_message(owner, f"Message from @{message.chat.username}\n\n{message.text}")
        return
    start(message)
