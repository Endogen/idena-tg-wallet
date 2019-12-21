import idena.emoji as emo
import idena.utils as utl
import logging

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from idena.plugin import IdenaPlugin


class Kill(IdenaPlugin):

    def __enter__(self):
        self.add_handler(CallbackQueryHandler(self._callback))
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

        update.message.reply_text(
            text="Do you really want to kill your identity?",
            reply_markup=self._confirm_button(address["result"]))

    def _confirm_button(self, address):
        msg = "💀 Confirm killing your identity"
        menu = utl.build_menu([InlineKeyboardButton(msg, callback_data=address)])
        return InlineKeyboardMarkup(menu, resize_keyboard=True)

    def _callback(self, bot, update):
        query = update.callback_query
        message = query.message

        kill = self.api().kill_identity(query.data)

        if "error" in kill:
            error = kill["error"]["message"]
            msg = f"{emo.ERROR} Couldn't kill identity: {error}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return

        msg = f"{emo.CHECK} Your identity was killed"
        message.edit_text(msg, parse_mode=ParseMode.MARKDOWN)

        bot.answer_callback_query(query.id, "Done")
