import idena.emoji as emo
import logging

from telegram import ParseMode
from pycoingecko import CoinGeckoAPI
from idena.plugin import IdenaPlugin


class Price(IdenaPlugin):

    CG_ID = "idena"
    CG_URL = "https://www.coingecko.com/coins/idena"

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        reply = "DNA price in BTC\n\n"

        try:
            result = CoinGeckoAPI().get_coin_ticker_by_id(self.CG_ID)
        except Exception as e:
            error = f"{emo.ERROR} Could not retrieve price"
            update.message.reply_text(error)
            logging.error(e)
            self.notify(e)
            return

        for data in result["tickers"]:
            base = data["base"]
            target = data["target"]

            if base == "DNA" and target == "BTC":
                exchange = data["market"]["name"]
                price = f"{data['last']:.8f}"

                reply += f"{exchange:<10}{price}\n"

        cg_link = f"\n[Details on CoinGecko]({self.CG_URL})"

        update.message.reply_text(
            text=f"`{reply}`{cg_link}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)
