import idena.emoji as emo

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Address(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        address = self.chk(self.api().address())

        if not address:
            msg = f"{emo.ERROR} Couldn't retrieve address. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        update.message.reply_text(f"`{address}`", parse_mode=ParseMode.MARKDOWN)
