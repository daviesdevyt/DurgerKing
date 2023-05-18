from flask import Flask, request, render_template, Response, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sellix import Sellix
from flask_migrate import Migrate
import os, dotenv
from datetime import datetime, timedelta
from .config import packages, url, view_counts, bot_token, owner
from telebot import TeleBot

dotenv.load_dotenv()

client = Sellix(os.getenv("API_KEY"))

app = Flask(__name__, template_folder="./static", static_url_path='', 
            static_folder='./static')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

gateways = ["ETHEREUM", "BINANCE_COIN", "BITCOIN", "BITCOIN_CASH", "LITECOIN", "MONERO", "SOLANA", "USDT", "USDC", "POLYGON", "TRON"]
tags = ["eth", "bnb", "btc", "bch", "ltc", "xmr", "sol", "usdt", "usdc", "matic", "trx"]

from .models import User

bot = TeleBot(bot_token, parse_mode="HTML")

@app.route("/")
def home():
    user_id = request.args.get("user_id")
    if not user_id:
        uname = bot.get_me().username
        return Response(f"Could not access this page. Got to <a href='t.me/{uname}'>@{uname}</a>")
    return render_template("index.html", tgid=user_id, packages_details=packages, packages=enumerate(packages.keys()), gateways=enumerate(gateways), view_counts=view_counts, tags=tags)

@app.route("/make-order", methods=["POST"])
def pay():
    request_data = request.get_json()
    try:
        email = request_data["email"]
        telegram_id = request_data["tgid"]
        if email == "":
            return jsonify("Your email is required")
        package = request_data["package"]
        timing = request_data['timing']
        gateway = request_data.get('gateway')
        _gateways = gateways.copy()
        if gateway:
            _gateways = None
        cost = packages[package][timing]
    except Exception as e:
        return jsonify(f"A error occured. Please refresh if the problem persists")
    res = client.create_payment(title="Your Order", value=cost, currency="USD", email=email,
                                white_label=False, gateway=gateway, gateways=_gateways, return_url=url+"/success",
                                custom_fields={"tgid":telegram_id, "p":package, "t":timing}, webhook=url+"/paid")
    return jsonify(res["url"])

@app.route("/success", methods=["GET"])
def customer_paid_page():
    return Response("<h3>Payment successful. You can go back to the telegram now</h3>")

@app.route("/paid", methods=["POST"])
def customer_paid_webhook():
    request_res = request.get_json(silent=True)
    if request_res:
        if request_res.get("event") == "order:paid":
            try:
                request_data = request_res["data"]
                telegram_id = request_data["custom_fields"]["tgid"]
                package = request_data["custom_fields"]["p"]
                timing = request_data["custom_fields"]["t"]
                duration = 7 if timing == "w" else 30
                u = add_or_update_user(telegram_id, package, duration)
                bot.send_message(telegram_id, "Thank you for your order! Your advertisements will be active & live within 24 - 48 Hours!\nYou will receive a notification when your subscription begins.")
                bot.send_message(owner, f"Just got an order from telegram user @{bot.get_chat(u.id).username}.\n\nOrder details:\n"\
                                    f"{package} Groups\nExpiring: {u.end_time.strftime('%I:%M %p %d %b, %Y')}\n\nYou will be notified when their message comes")
            except:
                invoice_url = "https://dashboard.sellix.io/invoices/"+request_data["status_history"][1]["invoice_id"]
                bot.send_message(owner, f"An order was paid but it seems the person didn't pay from the bot or there has been a mixup somewhere.\n\nGo to your <a href='{invoice_url}'>sellix dashboard</a> to see the invoice")
    return Response(status=200)

@app.route("/add-sub", methods=["GET", "POST"])
def add_sub():
    messages = []
    if request.method == "POST":
        try:
            tgid = request.form["tgid"]
            if int(tgid) != owner:
                raise Exception()
            user_id = request.form["user_id"]
            package = request.form["package"]
            date = request.form.get("enddate")
            frequency = request.form["freq"]
            duration = 7 if frequency == "w" else 30
            if date:
                date = datetime.strptime(f"{date}", '%Y-%m-%d')
            bot.get_chat(user_id)
            add_or_update_user(user_id, package, duration, etime=date)
            messages.append(("User added successfully", "success"),)
        except:
            messages.append(("An error occured", "danger"),)
        return render_template("add-sub.html", tg_id=tgid, packages=packages, flash=messages, user_id=None, username=None)
    uid = request.args.get("user_id")
    username = None
    if uid:
        username = bot.get_chat(uid).username
    return render_template("add-sub.html", tg_id=request.args.get("tg_id"), packages=packages, flash=messages, user_id=uid, username=username)

def add_or_update_user(telegram_id, package, duration, stime = datetime.now(), etime=None):
    user = db.session.query(User).get(int(telegram_id))
    if user:
        user.package = package
        user.start_time = stime
        if not etime:
            etime = max(user.end_time, stime)+timedelta(duration)
        user.end_time = etime
    else:
        if not etime:
            etime = stime+timedelta(duration)
        user = User(id=int(telegram_id), package=package, start_time=stime, end_time=etime, username=bot.get_chat(telegram_id).username)
        db.session.add(user)
    db.session.commit()
    return user