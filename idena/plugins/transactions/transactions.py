import idena.emoji as emo
import idena.utils as utl
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Transactions(IdenaPlugin):

    _URL = "https://scan.idena.io/tx?tx="

    hash = None
    count = None

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
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

        address = address["result"]

        if not self.count:
            self.count = self.config.get("trx_display")

        # ----- Pending Transactions -----

        if args and args[0].lower() == "pending":
            pending = self.api().pending_transactions(address, self.count)

            if "error" in pending:
                error = pending["error"]["message"]
                msg = f"{emo.ERROR} Couldn't retrieve pending transactions: {error}"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                logging.error(msg)
                return

            pending = pending["result"]["transactions"]

            if not pending:
                msg = f"{emo.INFO} No pending transactions"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                return

            self.count = len(pending) if len(pending) < self.count else self.count

            current = 0
            for transaction in pending:
                if current > self.count:
                    break
                else:
                    current += 1

                self._create_message(update, transaction)

            return

        transactions = self.api().transactions(address, self.count)

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
        icon = f"{emo.QUESTION}"

        if type == "sendTx":
            icon = f"{emo.SEND}"
        elif type == "send":
            icon = f"{emo.MONEY}"
        elif type == "invite":
            icon = f"{emo.SPEAKING}‍"
        elif type == "submitFlip":
            icon = f"{emo.PICTURE}"
        elif type == "online":
            icon = f"{emo.GREEN}"
        elif type == "offline":
            icon = f"{emo.RED}"
        elif type == "submitLongAnswers":
            icon = f"{emo.LONG}"
        elif type == "submitShortAnswers":
            icon = f"{emo.SHORT}"
        elif type == "evidence":
            icon = f"{emo.EYE}"
        elif type == "submitAnswersHash":
            icon = f"{emo.IDENTITY}"

        msg = f"`Type: {icon} {type}`\n" \
              f"`Date: {utl.unix2datetime(date)}`\n" \
              f"`Link: `[Link to Block Explorer]({link})"

        update.message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)
