import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Address(IdenaPlugin):

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

        msg = f"{emo.DNA} Your DNA address"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

        msg = f"`{address['result']}`"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
