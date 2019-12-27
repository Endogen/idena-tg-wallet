import idena.emoji as emo
import idena.utils as utl
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


# TODO: Add pending transactions
class Transactions(IdenaPlugin):

    _URL = "https://scan.idena.io/tx?tx="

    hash = None
    count = None
    address = None

    def execute(self, bot, update, args):
        kw_list = utl.get_kw(args)

        if "hash" in kw_list:
            self.hash = kw_list["hash"]

            transaction = self.api().transaction(self.hash)

            if "error" in transaction:
                error = transaction["error"]["message"]
                msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                logging.error(msg)
                return

            transaction = transaction["result"]

            self._create_message(update, transaction)
            return

        if "count" in kw_list:
            try:
                self.count = int(kw_list["count"])
            except:
                msg = f"{emo.ERROR} Couldn't convert 'count' parameter to Integer"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                logging.error(msg)
                return

        address = self.api().address()

        if "error" in address:
            error = address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        self.address = address["result"]

        if not self.count:
            self.count = self.config.get("trx_display")

        transactions = self.api().transactions(self.address, self.count)

        if "error" in transactions:
            error = transactions["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve transactions: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        transactions = transactions["result"]["transactions"]

        self.count = len(transactions) if len(transactions) < self.count else self.count

        current = 0
        for transaction in transactions:
            if current > self.count:
                break
            else:
                current += 1

            self._create_message(update, transaction)

    def _create_message(self, update, transaction):
        type = transaction["type"]
        date = transaction["timestamp"]
        link = f"{self._URL}{transaction['hash']}"

        msg = f"`Type: {type}`\n" \
              f"`Date: {utl.unix2datetime(date)}`\n" \
              f"`Link: `[Link to Block Explorer]({link})"

        update.message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)
