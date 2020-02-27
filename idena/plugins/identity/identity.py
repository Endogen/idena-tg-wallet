import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Identity(IdenaPlugin):

    @IdenaPlugin.owner
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

        msg = f"*General*\n"
        msg += f"` {'Age:':<13} {identity['age']}`\n"
        msg += f"` {'State:':<13} {identity['state']}`\n"
        msg += f"` {'Online:':<13} {identity['online']}`\n"
        msg += f"` {'Invites:':<13} {identity['invites']}`\n"
        msg += f"` {'Penalty:':<13} {identity['penalty']}`\n"
        msg += f"` {'Generation:':<13} {identity['generation']}`\n\n"
        msg += f"*Flips*\n"
        msg += f"` {'Required:':<13} {identity['requiredFlips']}`\n"
        msg += f"` {'Made:':<13} {identity['madeFlips']}`\n"
        msg += f"` {'Qualified:':<13} {identity['totalQualifiedFlips']}`\n"
        msg += f"` {'Short Points:':<13} {identity['totalShortFlipPoints']}`"

        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
