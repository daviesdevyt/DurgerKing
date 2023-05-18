import os, dotenv
dotenv.load_dotenv()

prod_url = "https://adbothost.com"
test_url = "https://"
url = prod_url
owner = int(os.getenv("owner"))
bot_token = os.getenv("BOT_TOKEN")
packages = {
    "250": {
        "w": "30",
        "m": "80"
    },
    "1000": {
        "w": "60",
        "m": "150"
    },  
    "1500": {
        "w": "80",
        "m": "200"
    },
    "2500": {
        "w": "120",
        "m": "300"
    },
    "5000": {
        "w": "180",
        "m": "500"
    }
}
view_counts = [("2,500 - 3,000", "10,000 - 12,000 "), ("6,000 - 7,500", "24,000 - 30,000"), ("36,000 - 45,000", "9,000 - 12,000"), ("15,000 - 20,000", "60,000 - 80,000"), ("30,000 - 35,000", "100,000 - 150,000")]
