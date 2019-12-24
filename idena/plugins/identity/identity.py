import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Identity(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if not args:
            address = self.api().address()

            if "error" in address:
                error = address["error"]["message"]
                msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                logging.error(msg)
                return

            address = address["result"]

        elif len(args) == 1:
            address = args[0]

        else:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        identity = self.api().identity(address)

        if "error" in identity:
            error = identity["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve identity: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        identity = identity["result"]

        msg = f"Invites: {identity['invites']}\n" \
              f"Age: {identity['age']}\n" \
              f"State: {identity['state']}\n" \
              f"Required Flips: {identity['requiredFlips']}\n" \
              f"Made Flips: {identity['madeFlips']}\n" \
              f"Qualified Flips: {identity['totalQualifiedFlips']}\n" \
              f"Short Flip Points: {identity['totalShortFlipPoints']}\n" \
              f"Flips: {identity['flips']}\n" \
              f"Online: {identity['online']}\n" \
              f"Generation: {identity['generation']}\n" \
              f"Code: {identity['code']}\n" \
              f"Penalty: {identity['penalty']}\n"

        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
