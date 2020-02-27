import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Offline(IdenaPlugin):

    @IdenaPlugin.owner
    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        offline = self.api().go_offline()

        if "error" in offline:
            error = offline["error"]["message"]
            msg = f"{emo.ERROR} Couldn't go offline: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        update.message.reply_text(f"{emo.CHECK} Node is offline", parse_mode=ParseMode.MARKDOWN)
