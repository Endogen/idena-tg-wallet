import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Import(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if len(args) != 2:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        import_key = self.api().import_key(args[0], args[1])

        if "error" in import_key:
            error = import_key["error"]["message"]
            msg = f"{emo.ERROR} Can't export identity: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        msg = f"{emo.BUST} Identity successfully imported"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
