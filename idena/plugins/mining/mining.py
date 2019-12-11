import idena.emoji as emo

from telegram import ParseMode
from idena.plugin import IdenaPlugin


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
            mining = self.chk(self.api().go_online())
        elif argument == "off":
            mining = self.chk(self.api().go_offline())
        else:
            mining = None

        if not mining:
            msg = f"{emo.ERROR} Couldn't set mining to `{argument}`. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        update.message.reply_text(f"`{mining}`", parse_mode=ParseMode.MARKDOWN)
