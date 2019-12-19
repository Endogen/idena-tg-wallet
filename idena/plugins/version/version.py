import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Version(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        node = self.api().node_version()

        if "error" in node:
            error = node["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve node version: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        node = node["result"]

        msg = f"Node Version: `{node}`"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
