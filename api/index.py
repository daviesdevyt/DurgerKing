from flask import Flask, request, render_template, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading
from flask_migrate import Migrate

app = Flask(__name__, template_folder="./static",static_url_path='', 
            static_folder='./static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fsnnluat:t67qU_x6IxPN-EoKcFmhRCD54we9qz30@mahmud.db.elephantsql.com/fsnnluat'
app.config['SECRET_KEY'] = '1f601a5ffe473ae4da49cd43ec646d3f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User
from .bot import bot, owner, edit_message

@app.route("/")
def home():
    user_id = request.args.get("user_id")
    if not user_id:
        return Response("Could not access this page. Got to @bot")
    return render_template("index.html", user_id=user_id)

@app.route("/subscribed")
def success():
    uid = request.form["custom_fields"]["user_id"]
    user = User(uid=int(uid))
    message = bot.send_message(uid, "Thank you for your order!\nYour advertisements will be active & live within 24 - 48 Hours!\nYou will receive a notification when your subscription begins.")
    edit_message(message)
    bot.send_message(owner, f"@{bot.get_chat(uid).username} just subscribed for {request.form['product_title']}. The message will come soon")
    db.session.add(user)
    db.session.commit()
    return Response("Subscription sucessful")

def start_poll():
    print("Started bot")
    bot.infinity_polling()

threading.Thread(target=start_poll, daemon=True).start()