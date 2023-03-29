from flask import Flask, request, render_template, Response, jsonify, abort, redirect
from flask_sqlalchemy import SQLAlchemy
import telebot, time
from sellix import Sellix
from flask_migrate import Migrate
import os, dotenv, json, requests
from .config import packages, url

dotenv.load_dotenv()

client = Sellix(os.getenv("API_KEY"))

app = Flask(__name__, template_folder="./static",static_url_path='', 
            static_folder='./static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fsnnluat:t67qU_x6IxPN-EoKcFmhRCD54we9qz30@mahmud.db.elephantsql.com/fsnnluat'
app.config['SECRET_KEY'] = '1f601a5ffe473ae4da49cd43ec646d3f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

gateways = ["ETHEREUM", "BINANCE_COIN", "BITCOIN", "USDT", "USDC", "POLYGON", "TRON", "BINANCE"]

from .models import User
from .bot import bot, owner, edit_message

@app.route("/")
def home():
    user_id = request.args.get("user_id")
    if not user_id:
        return Response(f"Could not access this page. Got to @{bot.get_me().username} on telegram")
    return render_template("index.html", tgid=user_id)

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
    try:
        email = request.form["email"]
        telegram_id = request.form["tgid"]
        if email == "":
            return Response("Your email is required")
        package = request.form["package"]
        timing = request.form['timing']
        cost = packages[package][timing]
    except Exception as e:
        return Response(f"Invalid request: {e}")
    res = client.create_payment(title="Your Order", value=cost, currency="USD", email=email,
                                white_label=False, gateways=gateways, return_url=request.referrer+"success",
                                custom_fields={"tgid":telegram_id}, webhook_url=request.referrer+"success")
    return redirect(res["url"])

@app.route("/success", methods=["GET", "POST"])
def customer_paid():
    if request.method == "POST":
        telegram_id = request.form["custom_fields"]["tgid"]
        user = User.query.get(int(telegram_id))
        if not user:
            user = User(uid=int(telegram_id))
            db.session.add(user)
            db.session.commit()
        bot.send_message(telegram_id, "Thank you for your order! Your advertisements will be active & live within 24 - 48 Hours!\nYou will receive a notification when your subscription begins.")
    return Response("<h3>Payment successful. You can go back to the telegram now</h3>")

WEBHOOK_URL = url+"/telegram"

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(url=WEBHOOK_URL)