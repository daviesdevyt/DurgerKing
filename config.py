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
