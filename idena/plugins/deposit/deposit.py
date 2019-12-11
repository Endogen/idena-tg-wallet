import os
import idena.emoji as emo
import idena.constants as con

from telegram import ParseMode
from idena.plugin import IdenaPlugin
from MyQR import myqr


class Deposit(IdenaPlugin):

    QRCODES_DIR = "qr_codes"
    TRON_LOGO = "idena.png"

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        user_id = update.effective_user.id

        # Create directory for qr-code images
        qr_dir = os.path.join(self.get_plg_path(), self.QRCODES_DIR)
        os.makedirs(qr_dir, exist_ok=True)

        # Get file and path of qr-code image
        qr_name = f"{user_id}.png"
        qr_code = os.path.join(qr_dir, qr_name)

        logo = os.path.join(self.get_plg_path(), con.DIR_RES, self.TRON_LOGO)

        address = self.chk(self.api().address())

        if not address:
            msg = f"{emo.ERROR} Couldn't retrieve address. Node offline?"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            return

        myqr.run(
            address,
            version=1,
            level='H',
            picture=logo,
            colorized=True,
            contrast=1.0,
            brightness=1.0,
            save_name=qr_name,
            save_dir=qr_dir)

        with open(qr_code, "rb") as qr_pic:
            update.message.reply_photo(
                photo=qr_pic,
                caption=f"`{address}`",
                parse_mode=ParseMode.MARKDOWN)
