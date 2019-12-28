import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Balance(IdenaPlugin):

    def __enter__(self):
        if self.config.get("balance_check", "active"):
            interval = self.config.get("balance_check", "interval")
            self.repeat_job(self._balance_check, interval)
        return self

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        address = self.api().address()

        if "error" in address:
            error = address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        address = address["result"]

        balance = self.api().balance(address)

        if "error" in balance:
            error = balance["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve balance: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        balance = balance["result"]

        if not balance:
            msg = f"{emo.ERROR} Couldn't retrieve balance: No funds"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        try:
            balance = f"{float(balance['balance']):.2f}"
        except:
            balance = 0

        msg = f"Balance: `{balance}` DNA"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

    def _balance_check(self, bot, job):
        address = self.api().address()

        if "error" in address:
            error = address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            logging.error(msg)
            return

        address = address["result"]

        balance = self.api().balance(address)

        if "error" in balance:
            error = balance["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve balance: {error}"
            logging.error(msg)
            return

        balance = balance["result"]

        if not balance:
            msg = f"{emo.ERROR} Couldn't retrieve balance: No funds"
            logging.error(msg)
            return

        try:
            balance = balance["balance"]
            balance = float(balance)
        except Exception as e:
            logging.error(f"Balance check error: {e}")
            return

        # ----- Check if balance changed -----

        threshold = self.config.get("balance_check", "threshold")
        saved_balance = self.config.get("balance_check", "balance")

        if not saved_balance:
            saved_balance = 0

        # Check if threshold reached
        if balance <= (saved_balance + threshold):
            # Save new balance
            self.config.set(balance, "balance_check", "balance")
            print("END")
            return

        # Send "balance changed" message to admins
        for admin in self.global_config.get("admin", "ids"):
            try:
                msg = f"{emo.BELL} Balance: `{balance:.2f}` DNA"
                bot.send_message(admin, msg, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                msg = f"Couldn't send 'balance changed' message to ID {str(admin)}: {e}"
                logging.warning(msg)

        # Save new balance
        self.config.set(balance, "balance_check", "balance")
