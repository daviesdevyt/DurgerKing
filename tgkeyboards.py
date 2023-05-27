from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from config import url, owner

def start_inline_markup(user_id):
    web_app = WebAppInfo(url=url+f"?user_id={user_id}")
    order_inline_btn = InlineKeyboardButton("ORDER NOW", web_app=web_app)
    account_inline_btn = InlineKeyboardButton("ACCOUNT", callback_data="account")
    support_inline_btn = InlineKeyboardButton("SUPPORT", url="https://t.me/adbothost3")
    start_markup = InlineKeyboardMarkup()
    start_markup.add(order_inline_btn)
    start_markup.row(account_inline_btn, support_inline_btn)
    return start_markup

view_tracking = InlineKeyboardButton("View tracking", callback_data="view_tracking")
manage_subscription = InlineKeyboardButton("Manage subscription", callback_data="manage_sub")

account_markup = InlineKeyboardMarkup()
account_markup.add(view_tracking)
account_markup.row(manage_subscription)
account_markup.row(InlineKeyboardButton("Edit bot", callback_data="edit_bot"))


edit_bot_markup = InlineKeyboardMarkup()
edit_bot_markup.add(InlineKeyboardButton("Edit Profile Pic", callback_data="bot_profile_pic"), InlineKeyboardButton("Edit Bio", callback_data="bot_bio"))
edit_bot_markup.add(InlineKeyboardButton("Edit Username", callback_data="bot_username"), InlineKeyboardButton("Set response", callback_data="bot_response"))
edit_bot_markup.add(InlineKeyboardButton("Change message", callback_data="edit_message"))
edit_bot_markup.add(InlineKeyboardButton("back", callback_data="account"))

def back_btn(step: str):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("back", callback_data=step)
    markup.add(btn)
    return markup

class Admin:
    kb = InlineKeyboardMarkup()
    get_all = InlineKeyboardButton("See all subscriptions", callback_data="admin_get_all")
    new_sub_form = InlineKeyboardButton("Add subscriber", web_app=WebAppInfo(url+"/add-sub?tg_id="+str(owner)))
    def back_btn(step: str):
        back_btn = InlineKeyboardButton("Back", callback_data=step)
        return back_btn

    kb.add(get_all)
    kb.add(new_sub_form)

    view_sub_back = InlineKeyboardButton("Back", callback_data="admin_get_all")