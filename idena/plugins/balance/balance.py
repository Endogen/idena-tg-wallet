import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Balance(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        address = self.api().address()

        if "error" in address:
            error = address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        address = address["result"]

        balance = self.api().balance(address)

        if "error" in balance:
            error = balance["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve balance: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        balance = balance["result"]

        if not balance:
            msg = f"{emo.ERROR} Couldn't retrieve balance: No funds"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        try:
            balance = f"{float(balance['balance']):.2f}"
        except Exception as e:
            balance = 0

        msg = f"Balance: `{balance}` DNA"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
