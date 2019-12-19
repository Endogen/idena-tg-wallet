import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


# TODO: go_online() and go_offline() needs an argument?!?
# TODO: Maybe provide two commands (go_online % go_offline)
class Mining(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if len(args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        argument = args[0].lower()

        if argument == "on":
            mining = self.api().go_online(self.api().address()["result"])
        elif argument == "off":
            mining = self.api().go_offline(self.api().address()["result"])
        else:
            mining = {"error": {"message": "Only 'on' and 'off' are valid values"}}

        if "error" in mining:
            error = mining["error"]["message"]
            msg = f"{emo.ERROR} Couldn't set mining to *{argument}*: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        update.message.reply_text(f"`{mining['result']}`", parse_mode=ParseMode.MARKDOWN)
