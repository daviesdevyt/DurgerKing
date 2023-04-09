from flask import Flask, request, render_template, Response, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import telebot, time
from sellix import Sellix
from flask_migrate import Migrate
import os, dotenv
from datetime import datetime, timedelta
from .config import packages, url

dotenv.load_dotenv()

client = Sellix(os.getenv("API_KEY"))

app = Flask(__name__, template_folder="./static", static_url_path='', 
            static_folder='./static')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

gateways = ["ETHEREUM", "BINANCE_COIN", "BITCOIN", "BITCOIN_CASH", "LITECOIN", "MONERO", "SOLANA", "USDT", "USDC", "POLYGON", "TRON"]

from .models import User
from .bot import bot, owner
WEBHOOK_URL = url+"/telegram"

@app.route("/set")
def set_wh():
    try:
        bot.remove_webhook()
        time.sleep(0.5)
        bot.set_webhook(url=WEBHOOK_URL)
        return ""
    except Exception as e:
        return "Invalid "+str(e)

@app.route("/")
def home():
    user_id = request.args.get("user_id")
    if not user_id:
        return Response(f"Could not access this page. Got to @{bot.get_me().username} on telegram")
    return render_template("index.html", tgid=user_id, packages_details=packages, packages=enumerate(packages.keys()), gateways=gateways)

@app.route("/telegram", methods=["POST"])
def telegram_bot():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:   
        abort(403)

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
                                white_label=False, gateway=gateway, gateways=_gateways, return_url=request.referrer+"success",
                                custom_fields={"tgid":telegram_id, "p":package, "t":timing}, webhook_url=request.referrer+"success")
    return jsonify(res["url"])

@app.route("/success", methods=["GET", "POST"])
def customer_paid():
    if request.method == "POST":
        telegram_id = request.form["custom_fields"]["tgid"]
        package = request.form["custom_fields"]["p"]
        timing = request.form["custom_fields"]["t"]
        duration = 7 if timing == "w" else 30
        stime = datetime.now()
        etime = stime+timedelta(duration)
        add_or_update_user(telegram_id, package, stime, etime)
        bot.send_message(telegram_id, "Thank you for your order! Your advertisements will be active & live within 24 - 48 Hours!\nYou will receive a notification when your subscription begins.")
        bot.send_message(owner, f"Just got an order from telegram user @{bot.get_chat(telegram_id).username}. His message is on its way")
    return Response("<h3>Payment successful. You can go back to the telegram now</h3>")

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
            date = request.form["date"]
            time = request.form.get("stime")
            if not time: time = "00:00"
            frequency = request.form["freq"]
            duration = 7 if frequency == "w" else 30
            stime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
            etime = stime+timedelta(duration)
            bot.get_chat(user_id)
            add_or_update_user(user_id, package, stime, etime)
            messages.append(("User added successfully", "success"),)
        except:
            messages.append(("An error occured", "danger"),)
        return render_template("add-sub.html", user_id=tgid, packages=packages, flash=messages)
    return render_template("add-sub.html", user_id=request.args.get("user_id"), packages=packages, flash=messages)

def add_or_update_user(telegram_id, package, stime, etime):
    user = User.query.get(int(telegram_id))
    if not user:
        user = User(id=int(telegram_id), package=package, start_time=stime, end_time=etime)
        db.session.add(user)
    else:
        user.package = package
        user.start_time = stime
        user.end_time = etime
    db.session.commit()