from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
import requests
import bs4

from token_settings import token

updater = Updater(token)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {update.effective_user.first_name}, asaxiy.uzdan nima qidiramiz?')


def search_handle(update: Update, context: CallbackContext):
    user_product = update.message.text.strip()
    url = f"https://asaxiy.uz/product?key={user_product}"

    page = requests.get(url, timeout=10)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    products = soup.find_all("div", attrs={"class": "col-6 col-xl-3 col-md-4"}, limit=10)

    for product in products:
        image_link = product.find("div", attrs={"class": "product__item-img"}).find("img")['data-src']
        title = product.find("h5", attrs={"class": "product__item__info-title"}).text
        price = product.find("span", attrs={"class": "product__item-price"}).text

        if image_link[-5:] == '.webp':
            image_link = product.find("div", attrs={"class": "product__item-img"}).find("img")['data-src'][0:-5]

        context.bot.send_photo(update.effective_user.id, image_link, f"{title}\n"
                                                                     f"Narxi: {price}\n")


def error_handle(update: Update, context: CallbackContext):
    update.message.reply_text("To'g'ri mahsulot nomini kiriting!")


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, search_handle))
dispatcher.add_handler(MessageHandler(Filters.all, error_handle))

updater.start_polling()
updater.idle()
