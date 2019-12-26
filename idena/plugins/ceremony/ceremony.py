import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Ceremony(IdenaPlugin):

    def execute(self, bot, update, args):
        ceremony = self.api().ceremony_intervals()

        if "error" in ceremony:
            error = ceremony["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        ceremony = ceremony["result"]

        msg = f"*Durations in seconds*\n"
        msg += f"` {'Flip Lottery:':<19} {ceremony['FlipLotteryDuration']}`\n"
        msg += f"` {'Short Session:':<19} {ceremony['ShortSessionDuration']}`\n"
        msg += f"` {'Long Session:':<19} {ceremony['LongSessionDuration']}`\n"
        msg += f"` {'After Long Session:':<19} {ceremony['AfterLongSessionDuration']}`"

        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
