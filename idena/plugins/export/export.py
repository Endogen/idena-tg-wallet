import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Export(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if len(args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        export = self.api().export_key(args[0])

        if "error" in export:
            error = export["error"]["message"]
            msg = f"{emo.ERROR} Can't export identity: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        msg = f"{emo.KEY} Private key to identity"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

        key = export["result"]
        update.message.reply_text(f"`{key}`", parse_mode=ParseMode.MARKDOWN)
