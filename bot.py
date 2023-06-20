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

@bot.message_handler(func=lambda msg: True)
def new_message(message: Message):
    user = session.query(User).get(message.chat.id)
    if not user or user.end_time < datetime.now():
        bot.send_message(message.chat.id, "You have no active subscription.\nClick \"🛍️ORDER NOW\" below to choose a subscription")
        return
    if message.text == "⚙️SUBSCRIPTION":
        end = user.end_time.strftime("%I:%M %p %d %b, %Y")
        bot.send_message(message.chat.id, f"User ID: {message.chat.id}\nUsername: {message.chat.username}\n"
                            f"\nPackage: {user.package} Groups\nExpiring: {end}", parse_mode="markdown")
    elif message.text == "👁️VIEW TRACKING":
        user_message = user.message
        if user_message or user_message != "":
            msg_id, chat_id = user_message.split(":")
            bot.forward_message(message.chat.id, chat_id, msg_id)
        else:
            bot.send_message(message.chat.id, 'You have no current message set')
    elif message.text == "🤖EDIT BOT":
        bot.send_message(message.chat.id, "Choose:", reply_markup=edit_bot_markup)
    elif message.text == "📞SUPPORT":
        bot.send_message(message.chat.id, "Contact @adhostbot3 by clicking the button below", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Contact", url="https://t.me/adbothost3")))

@bot.callback_query_handler(func=lambda call: call.message.text != None)
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
            kb.add(Admin.back_btn("admin_back"))
            bot.edit_message_text("What user do you want to see", message.chat.id, message.id, reply_markup=kb)

        elif data.startswith("view_sub"):
            _, uid = data.split(":")
            user = session.query(User).get(int(uid))
            if not user:
                bot.edit_message_text(message, f"User \"{uid}\" doesnt exist", reply_markup=InlineKeyboardMarkup().add(Admin.view_sub_back))
                return
            kb = InlineKeyboardMarkup()
            get_set = []
            if user.message:
                get_set.append(InlineKeyboardButton("Get message", callback_data=f"admin_getmsg_{user.message}"))
            get_set.append(InlineKeyboardButton("Set message", callback_data=f"admin_setmsg_{user.id}"))
            kb.add(*get_set)
            kb.add(InlineKeyboardButton("Edit subscription", web_app=WebAppInfo(url+"/add-sub?tg_id="+str(message.chat.id)+"&user_id="+uid)))
            kb.add(Admin.view_sub_back)
            end = user.end_time.strftime("%I:%M %p %d %b, %Y")
            bot.edit_message_text(f"User ID: {uid}\nUsername: @{user.username}\n"
                            f"\nPackage: {user.package} Groups\nExpiring: {end}",message.chat.id, message.id, reply_markup=kb)
        
        elif data.startswith("setmsg_"):
            user_id = data.strip("setmsg_")
            user_message = session.query(User).get(user_id).message
            if user_message:
                msg_id, chat_id = user_message.split(":")
                bot.forward_message(owner, chat_id, msg_id)
            bot.send_message(message.chat.id, "Previous message ☝️.\nSend or forward the new message you want to set\n\nUse /cancel to leave it unchanged")
            bot.register_next_step_handler(message, admin_set_message, user_id)

        elif data.startswith("getmsg_"):
            data = data.strip("getmsg_")
            msg_id, chat_id = data.split(":")
            bot.forward_message(owner, chat_id, msg_id)

        elif data == "back":
            bot.edit_message_text("<b>Welcome back Admin!!</b>\nWhat will you like to do today?", message.chat.id, message.id, reply_markup=Admin.kb)
        return

    user = session.query(User).get(message.chat.id)
    if not user or user.end_time < datetime.now():
        # web_app = WebAppInfo(url=url+f"?user_id={message.chat.id}")
        # order_inline_btn = InlineKeyboardButton("ORDER NOW", web_app=web_app)
        # markup = InlineKeyboardMarkup()
        # markup.add(order_inline_btn)
        bot.answer_callback_query(callback.id, "You have no active subscription.\nUse the button below to choose a subscription", True)
        # bot.edit_message_text(f"Your telegram ID: `{message.chat.id}`\n\nYou have no active subscription.\nUse the button below to choose a subscription",
        #                       message.chat.id, message.id, reply_markup=start_inline_markup(message.chat.id), parse_mode="markdown")
        return

    elif data == "edit_bot":
        bot.edit_message_text("Choose:", message.chat.id, message.id, reply_markup=edit_bot_markup)

    elif data == "bot_profile_pic":
        bot.edit_message_text("Send a photo\n\nUse /cancel to cancel", message.chat.id, message.id)
        bot.register_next_step_handler(message, new_bot_pic)

    elif data.startswith("bot_"):
        data = data[4:]
        bot.edit_message_text(f"Send a {data}\n\nUse /cancel to cancel", message.chat.id, message.id)
        bot.register_next_step_handler(message, new_bot_text, data)

    elif data == "edit_message":
        if user.last_changed_message:
            if (datetime.now() - user.last_changed_message).days < 2:
                bot.edit_message_text("You updated your message recently. You need to wait 48 hours before you can edit your message again",message.chat.id, message.id, reply_markup=back_btn("account"))
                return
        user_message = user.message
        if user_message or user_message != "":
            msg_id, chat_id = user_message.split(":")
            bot.forward_message(message.chat.id, chat_id, msg_id)
        bot.send_message(
            message.chat.id, f"{'That is your current message ☝️' if user_message else 'You have no current message set'}\n\nSend the new message you want to set\n\nUse /cancel to leave it unchanged", parse_mode="markdown")
        bot.register_next_step_handler(message, set_message)

    elif data.startswith("accept_change"):
        _, msg_id, chat_id = data.split(":")
        user.last_changed_message = datetime.now()
        user.message = f"{msg_id}:{chat_id}"
        session.commit()
        bot.forward_message(-1001984299345, chat_id, msg_id)
        bot.edit_message_text(f"Message updated\n\nYour changes will be viable within 24 hours", message.chat.id, message.id)
        bot.send_message(owner, f"Newest Message from @{message.chat.username}")
        bot.forward_message(owner, chat_id, msg_id)
    
    elif data == "decline_change":
        bot.edit_message_text("Changes have been declined", message.chat.id, message.id, reply_markup=back_btn("account"))

def new_bot_pic(message:Message):
    if message.text == "/cancel":
        cancel(message)
        return
    if not message.photo:
        bot.send_message(message.chat.id, "Please send a photo compressed")
        bot.register_next_step_handler(message, new_bot_pic)
        return
    photo = message.photo[1].file_id
    bot.send_photo(owner, photo, f"New bot profile photo for @{message.chat.username}")
    bot.send_message(message.chat.id, "Bot profile picture updated!", reply_markup=back_btn("edit_bot"))

def new_bot_text(message:Message, data):
    if message.text == "/cancel":
        cancel(message)
        return
    if not message.text:
        bot.send_message(message.chat.id, "Please send a text message")
        bot.register_next_step_handler(message, new_bot_text, data)
        return
    bot.send_message(owner, f"New bot {data} for @{message.chat.username}\n\n`{message.text}`", parse_mode="markdown")
    bot.send_message(message.chat.id, f"Bot {data} updated!", reply_markup=back_btn("edit_bot"))

def set_message(message: Message):
    if message.text == "/cancel":
        cancel(message)
        return
    msg_id, chat_id = message.id, message.chat.id
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Yes", callback_data=f"accept_change:{msg_id}:{chat_id}"), InlineKeyboardButton("No", callback_data="decline_change"))
    bot.send_message(message.chat.id, "Are you sure you want to make this change you will not be able to edit your message for 48 hours", reply_markup=kb)

def admin_set_message(message: Message, user_id):
    if message.text == "/cancel":
        cancel(message)
        return
    user = session.query(User).get(user_id)
    msg_id, chat_id = message.id, message.chat.id
    user.message = f"{msg_id}:{chat_id}"
    session.commit()
    bot.forward_message(-1001984299345, chat_id, msg_id)
    bot.send_message(message.chat.id, f"Message updated", reply_markup=InlineKeyboardMarkup().add(Admin.back_btn(f"admin_view_sub:{user.id}")))

@bot.message_handler(func=lambda message: True)
def echo_message(message: Message):
    start(message)

print("Started")
bot.infinity_polling()