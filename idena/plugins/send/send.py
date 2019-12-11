import logging
import idena.emoji as emo
import idena.constants as con

from telegram import ParseMode
from idena.plugin import IdenaPlugin


# TODO: Take in account the fee. Always the same?
class Send(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if len(args) != 2:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        amount = args[0]

        # Check if amount is valid
        try:
            float(amount)
        except:
            msg = f"{emo.ERROR} Provided amount is not valid"
            logging.info(f"{msg} - {update}")
            update.message.reply_text(msg)
            return

        to_address = args[1]
        from_address = self.chk(self.api().address())

        if not from_address:
            msg = f"{emo.ERROR} Couldn't retrieve address. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        balance = self.chk(self.api().balance(from_address))

        if not balance:
            msg = f"{emo.ERROR} Couldn't retrieve balance. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        balance = f"{float(balance['balance']):.2f}"

        send = self.chk(self.api().send(from_address, to_address, float(amount)))

        if not send:
            msg = f"{emo.ERROR} Couldn't send DNA. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return
