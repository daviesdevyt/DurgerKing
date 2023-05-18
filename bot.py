from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from tgkeyboards import *
from db import session, User
from config import bot_token, owner
from datetime import datetime

bot = TeleBot(bot_token, parse_mode="HTML")

start_message = "<b>Let’s get started</b> 🎉\n\nPlease tap the button below to subscribe!"

@bot.message_handler(commands=['help', 'start'])
def start(message: Message):
    bot.clear_step_handler(message)
    bot.reply_to(message, start_message,
                 reply_markup=start_inline_markup(message.chat.id))


@bot.message_handler(commands=["admin"], func=lambda msg: msg.chat.id == owner)
def admin(message: Message):
    bot.clear_step_handler(message)
    bot.send_message(
        message.chat.id, "<b>Welcome back Admin!!</b>\nWhat will you like to do today?", reply_markup=Admin.kb)

@bot.message_handler(commands=["cancel"])
def cancel(message: Message):
    bot.clear_step_handler(message)
    bot.send_message(message.chat.id, "Operation cancelled")


@bot.callback_query_handler(func=lambda call: call.data != None)
def account(callback: CallbackQuery):
    message = callback.message
    data = callback.data

    if data == "back":
        bot.clear_step_handler(message)
        bot.edit_message_text(start_message, chat_id=message.chat.id, message_id=message.id,
                              reply_markup=start_inline_markup(message.chat.id))
        return

    elif data.startswith("admin_") and message.chat.id == owner:
        data = data.strip("admin_")
        if data == "get_all":
            all_users = session.query(User).all()
            kb = InlineKeyboardMarkup()
            kb.add(*[InlineKeyboardButton("@"+str(user.username), callback_data=f"admin_view_sub:{user.id}") for user in all_users])
            bot.edit_message_text("What user do you want to see", message.chat.id, message.id, reply_markup=kb)

        elif data.startswith("view_sub"):
            _, uid = data.split(":")
            user = session.query(User).get(int(uid))
            if not user:
                bot.edit_message_text(message, f"User \"{uid}\" doesnt exist", reply_markup=InlineKeyboardMarkup().add(Admin.view_sub_back))
                return
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Get message", callback_data=f"admin_getmsg_{user.message}"))
            kb.add(InlineKeyboardButton("Edit subscription", web_app=WebAppInfo(url+"/add-sub?tg_id="+str(message.chat.id)+"&user_id="+uid)))
            kb.add(Admin.view_sub_back)
            end = user.end_time.strftime("%I:%M %p %d %b, %Y")
            bot.edit_message_text(f"User ID: {uid}\nUsername: @{user.username}\n"
                            f"\nPackage: {user.package} Groups\nExpiring: {end}",message.chat.id, message.id, reply_markup=kb)
        
        elif data.startswith("getmsg_"):
            data = data.strip("getmsg_")
            msg_id, chat_id = data.split(":")
            bot.forward_message(owner, chat_id, msg_id)
        elif data == "back":
            bot.edit_message_text("<b>Welcome back Admin!!</b>\nWhat will you like to do today?", message.chat.id, message.id, reply_markup=Admin.kb)
        return

    user = session.query(User).get(message.chat.id)
    if not user or user.end_time < datetime.now():
        web_app = WebAppInfo(url=url+f"?user_id={message.chat.id}")
        order_inline_btn = InlineKeyboardButton("ORDER NOW", web_app=web_app)
        markup = InlineKeyboardMarkup()
        markup.add(order_inline_btn)
        bot.edit_message_text(f"Your telegram ID: `{message.chat.id}`\n\nYou have no active subscription.\nUse the button below to choose a subscription",
                              message.chat.id, message.id, reply_markup=start_inline_markup(message.chat.id), parse_mode="markdown")
        return

    if data == "account":
        bot.clear_step_handler(message)
        bot.edit_message_text(f"Hello <b>{message.chat.username}</b>.\nWhat do you want to do today?",
                              message.chat.id, message.id, reply_markup=account_markup)

    elif data == "manage_sub":
        end = user.end_time.strftime("%I:%M %p %d %b, %Y")
        bot.edit_message_text(f"User ID: {message.chat.id}\nUsername: {message.chat.username}\n"
                              f"\nPackage: {user.package} Groups\nExpiring: {end}", message.chat.id, message.id, parse_mode="markdown", reply_markup=account_markup)

    elif data == "view_tracking":
        user_message = user.message
        if user_message or user_message == "":
            msg_id, chat_id = user_message.split(":")
            bot.forward_message(message.chat.id, chat_id, msg_id)
        else:
            bot.send_message(message.chat.id, 'You have no current message set')

    elif data == "edit_message":
        user_message = user.message
        if user_message or user_message == "":
            msg_id, chat_id = user_message.split(":")
            bot.forward_message(message.chat.id, chat_id, msg_id)
        bot.send_message(
            message.chat.id, f"{'That is your current message ☝️' if user_message else 'You have no current message set'}\n\nSend the new message you want to set\n\nUse /cancel to leave it unchanged", parse_mode="markdown")
        bot.register_next_step_handler(message, set_message)


def set_message(message: Message):
    if message.text == "/cancel":
        cancel(message)
        return
    user = session.query(User).get(message.chat.id)
    msg_id, chat_id = message.id, message.chat.id
    user.message = f"{msg_id}:{chat_id}"
    session.commit()
    bot.reply_to(message, f"Message updated\n\nYour changes will be viable within 24 hours",
                 parse_mode="markdown", reply_markup=account_markup)
    bot.send_message(
        owner, f"Newest Message from @{message.chat.username}", parse_mode="markdown")
    bot.forward_message(owner, chat_id, msg_id)


@bot.message_handler(func=lambda message: True)
def echo_message(message: Message):
    start(message)

bot.infinity_polling()