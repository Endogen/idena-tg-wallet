import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Stake(IdenaPlugin):

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

        balance = self.api().balance(address["result"])

        if "error" in balance:
            error = balance["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve balance: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        balance = f"{float(balance['result']['stake']):.2f}"

        msg = f"Stake: `{balance}` DNA"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
