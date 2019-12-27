import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Enode(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        enode = self.api().enode()

        if "error" in enode:
            error = enode["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve enode: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        msg = f"{emo.NETWORK} Enode value"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

        msg = f"`{enode['result']}`"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
