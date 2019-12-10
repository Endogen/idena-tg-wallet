import idena.emoji as emo

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Balance(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        address = self.chk(self.api().address())

        if not address:
            msg = f"{emo.ERROR} Couldn't retrieve address. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        balance = self.chk(self.api().balance(address))

        if not balance:
            msg = f"{emo.ERROR} Couldn't retrieve balance. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        balance = f"{float(balance['balance']):.2f}"

        msg = f"Balance: `{balance}` DNA"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
