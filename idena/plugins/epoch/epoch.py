import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Epoch(IdenaPlugin):

    @IdenaPlugin.owner
    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        epoch = self.api().epoch()

        if "error" in epoch:
            error = epoch["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve epoch info: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        epoch = epoch["result"]

        msg = f"`Epoch: {epoch['epoch']}`\n" \
              f"`Current Period: {epoch['currentPeriod']}`\n\n" \
              f"`Current Validation:\n{epoch['currentValidationStart']}`\n\n" \
              f"`Next Validation:\n{epoch['nextValidation']}`" \

        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
