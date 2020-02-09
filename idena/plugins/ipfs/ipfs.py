import idena.utils as utl
import idena.emoji as emo
import logging

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Ipfs(IdenaPlugin):

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        ipfs = self.api().ipfs_address()

        if "error" in ipfs:
            error = ipfs["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve IPFS address: {utl.esc_md(error)}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        msg = f"{emo.NETWORK} IPFS address"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

        msg = f"`{ipfs['result']}`"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
