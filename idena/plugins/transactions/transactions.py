import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


# TODO: Add pending transactions
# TODO: First argument wallet, second counter
# TODO: Show buttons to show details for each transaction
class Transactions(IdenaPlugin):

    def execute(self, bot, update, args):
        address = self.api().address()

        if "error" in address:
            error = address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        address = address["result"]


        transactions = self.api().transactions(address, count)