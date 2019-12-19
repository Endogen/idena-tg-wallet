import logging
import idena.emoji as emo

from telegram import ParseMode
from idena.plugin import IdenaPlugin


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
        from_address = self.api().address()

        if "error" in from_address:
            error = from_address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve sending address: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        from_address = from_address["result"]
        balance = self.api().balance(from_address)

        if "error" in balance:
            error = balance["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve balance: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        balance = balance["result"]["balance"]

        if float(balance) < float(amount):
            msg = f"{emo.ERROR} No sufficient funds. Balance is `{balance}` DNA"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        send = self.api().send(from_address, to_address, float(amount))

        if "error" in send:
            error = send["error"]["message"]
            msg = f"{emo.ERROR} Couldn't send DNA: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        msg = f"{emo.CHECK} Successfully sent"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
