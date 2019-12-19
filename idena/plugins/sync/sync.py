import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Sync(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        sync = self.api().sync_status()

        if "error" in sync:
            error = sync["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve sync status: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        sync = sync["result"]

        msg = f"Syncing: {str(sync['syncing'])}\n\n" \
              f"Current Block: {sync['currentBlock']}\n" \
              f"Highest Block: {sync['highestBlock']}\n\n" \
              f"Wrong Time: {sync['wrongTime']}"

        update.message.reply_text(f"`{msg}`", parse_mode=ParseMode.MARKDOWN)
