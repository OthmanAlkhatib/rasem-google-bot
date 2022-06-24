from telegram.ext import CommandHandler, Updater, CallbackContext
from telegram import Update
import requests
import json
import os
import logging
import sys

TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if MODE == "dev":
    def run():
        logger.info("Start in DEV mode")
        updater.start_polling()
elif MODE == "prod":
    def run():
        logger.info("Start in PROD mode")
        updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), url_path=TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format("rasem-google-bot", TOKEN))
else:
    logger.error("No mode specified")
    sys.exit(1)

headers1 = {
    "apikey": os.getenv("GOOGLE_API_1")
}
headers2 = {
    "apikey": os.getenv("GOOGLE_API_2")
}
def search_api(search_text):
    search_text = search_text.replace(" ", "%20")
    url = "https://api.apilayer.com/google_search?q={0}".format(search_text)

    payload = {}

    response = requests.request("GET", url, headers=headers1, data=payload)
    status_code = response.status_code
    if status_code == 429:
        response = requests.request("GET", url, headers=headers2, data=payload)

    result = json.loads(response.text)

    return result["organic"][0]["link"]


def search_handler(update: Update, context: CallbackContext):
    try:
        sh = update.message.text.split(" ", 1)
        link = search_api(sh[1])
    except Exception as error:
        if update.message.chat.username == "gehad100" :
            update.message.reply_text("قلي سيدي")
        else:
            update.message.reply_text("تفه")
        print(error)
        return
    
    update.message.reply_text(link)


if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("search", search_handler))

    run()



























