from flask import Flask, request, render_template, Response, jsonify
from sellix import Sellix
import os, dotenv, json

dotenv.load_dotenv()

client = Sellix(os.getenv("API_KEY"))

# gateways = ["PAYPAL", "ETHEREUM", "BINANCE_COIN", "BITCOIN", "BITCOIN_CASH", "LITECOIN", "SKRILL", "STRIPE", "PERFECT_MONEY", "CASH_APP",
#             "LEX_HOLDINGS_GROUP", "PAYDASH", "MONERO", "CONCORDIUM", "BITCOIN_LN", "NANO", "SOLANA", "RIPPLE", "USDT", "USDC", "PLZ", "POLYGON", "TRON", "BINANCE"]
gateways = ["ETHEREUM", "BINANCE_COIN", "BITCOIN", "USDT", "USDC", "POLYGON", "TRON", "BINANCE"]

with open("db.json") as f:
    products = json.load(f)

app = Flask(__name__, template_folder="./static",static_url_path='', 
            static_folder='./static')

@app.route("/")
def home():
    return render_template("index.html", product_ids=list(products), products=products)

@app.route("/make-order", methods=["GET", "POST"])
def pay():
    try:
        email = request.form["email"]
        if email == "":
            return Response("Your email is required")
        orders = json.loads(request.form["order_data"])
        total = 0
        for i in orders:
            total += float(products[str(i["id"])]["price"])/1000*i["count"]
    except Exception as e:
        return Response("Invalid request")
    res = client.create_payment(title="Your Order", value=total, currency="USD", email=email,
                                white_label=False, gateways=gateways, return_url=request.referrer+"success")
    return jsonify(res)

@app.route("/success")
def success():
    return Response("Your product is on its way !!")
