import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Online(IdenaPlugin):

    @IdenaPlugin.owner
    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        online = self.api().go_online()

        if "error" in online:
            error = online["error"]["message"]
            msg = f"{emo.ERROR} Couldn't go online: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        update.message.reply_text(f"{emo.CHECK} Node is online", parse_mode=ParseMode.MARKDOWN)
