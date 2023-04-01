from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from tgkeyboards import *
from models import User
from index import db, os
from datetime import datetime

bot = TeleBot(os.getenv("BOT_TOKEN"))
owner = 1289366093

@bot.message_handler(commands=['help', 'start'])
def start(message: Message):
    bot.reply_to(message, "Welcome to ad host bot",
                 reply_markup=start_inline_markup(message.chat.id))
    bot.clear_step_handler(message)

@bot.callback_query_handler(func=lambda call: call.data != None)
def account(callback: CallbackQuery):
    if callback.data == "back":
        bot.edit_message_text("Welcome to ad host bot", chat_id=callback.message.chat.id, message_id=callback.message.id)
        return
    
    if callback.data == "support":
        bot.edit_message_text("Contact for more info", callback.message.chat.id, callback.message.message_id, reply_markup=back_btn("back"))
        return

    user = User.query.get(callback.message.chat.id)
    if not user or user.end_time < datetime.now():
        bot.send_message(callback.message.chat.id, "You have no active subscription. Usen the \"ORDER NOW\" to choose a subscription")
        return
    
    if callback.data == "account":
        bot.send_message(callback.message.chat.id, f"Hello {callback.chat.username}.\nWhat do you want to do today?", reply_markup=account_markup)
    
    if callback.data == "edit_message":
        edit_message(callback.message)

@bot.message_handler(commands=["editmessage"])
def edit_message(message: Message):
    bot.send_message(message.chat.id, "Send the new message you want to set")
    bot.register_next_step_handler(message, set_message)

def set_message(message):
    user = User.query.get(message.chat.id)
    user.message = message.text
    db.session.commit()
    bot.reply_to(message, f"Message updated !! to {message.text}")
    bot.send_message(owner, f"Newest Message from @{message.chat.username}\n\n{message.text}")

@bot.message_handler(func=lambda message: True)
def echo_message(message: Message):
    start(message)

# bot.enable_save_next_step_handlers(delay=1)
# bot.load_next_step_handlers()