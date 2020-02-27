from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Start(IdenaPlugin):

    INTRO = "intro.md"

    @IdenaPlugin.owner
    @IdenaPlugin.threaded
    def execute(self, bot, update, args):
        user = update.effective_user

        intro = self.get_resource(self.INTRO)
        intro = intro.replace("{{firstname}}", user.first_name)

        update.message.reply_text(intro, parse_mode=ParseMode.MARKDOWN)
