from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from .config import url, owner

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
edit_message = InlineKeyboardButton("Edit message", callback_data="edit_message")
manage_subscription = InlineKeyboardButton("Manage subscription", callback_data="manage_sub")

account_markup = InlineKeyboardMarkup()
account_markup.add(view_tracking, edit_message)
account_markup.row(manage_subscription)


def back_btn(step: str):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("back", callback_data=step)
    markup.add(btn)
    return markup

class Admin:
    kb = InlineKeyboardMarkup()
    get_all = InlineKeyboardButton("See all subscriptions", callback_data="admin_get_all")
    new_sub_form = InlineKeyboardButton("Add subscriber", web_app=WebAppInfo(url+"/add-sub?user_id="+str(owner)))    
    back_btn = InlineKeyboardButton("Back", callback_data="admin_back")
    kb.add(get_all)
    kb.add(new_sub_form)

    @classmethod
    def get_kb(cls):
        return cls.kb
