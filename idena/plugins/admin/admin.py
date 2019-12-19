import os
import logging
import idena.utils as utl
import idena.emoji as emo

from telegram import ParseMode
from idena.config import ConfigManager
from idena.plugin import IdenaPlugin


class Admin(IdenaPlugin):

    @IdenaPlugin.owner
    @IdenaPlugin.private
    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if not args:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        command = args[0].lower()
        args.pop(0)

        plugin = args[0].lower()
        args.pop(0)

        # ---- Change configuration ----
        if command == "cfg":
            conf = args[0].lower()
            args.pop(0)

            get_set = args[0].lower()
            args.pop(0)

            # SET a config value
            if get_set == "set":
                # Get value for key
                value = args[-1].replace("__", " ")
                args.pop(-1)

                # Check value for boolean
                if value.lower() == "true" or value.lower() == "false":
                    value = utl.str2bool(value)

                # Check value for integer
                elif value.isnumeric():
                    value = int(value)

                # Check value for null
                elif value.lower() == "null" or value.lower() == "none":
                    value = None

                try:
                    if plugin == "-":
                        value = self.global_config.set(value, *args)
                    else:
                        cfg_file = f"{conf}.json"
                        plg_conf = self.get_cfg_path(plugin=plugin)
                        cfg_path = os.path.join(plg_conf, cfg_file)
                        ConfigManager(cfg_path).set(value, *args)
                except Exception as e:
                    logging.error(e)
                    msg = f"{emo.ERROR} {e}"
                    update.message.reply_text(msg)
                    return

                update.message.reply_text(f"{emo.CHECK} Config changed")

            # GET a config value
            elif get_set == "get":
                try:
                    if plugin == "-":
                        value = self.global_config.get(*args)
                    else:
                        cfg_file = f"{conf}.json"
                        plg_conf = self.get_cfg_path(plugin=plugin)
                        cfg_path = os.path.join(plg_conf, cfg_file)
                        value = ConfigManager(cfg_path).get(*args)
                except Exception as e:
                    logging.error(e)
                    msg = f"{emo.ERROR} {e}"
                    update.message.reply_text(msg)
                    return

                update.message.reply_text(value)

            # Wrong syntax
            else:
                update.message.reply_text(
                    text=f"Usage:\n{self.get_usage()}",
                    parse_mode=ParseMode.MARKDOWN)

        # ---- Manage plugins ----
        elif command == "plg":
            try:
                # Start plugin
                if args[0].lower() == "add":
                    res = self.add_plugin(plugin)

                # Stop plugin
                elif args[0].lower() == "remove":
                    res = self.remove_plugin(plugin)

                # Wrong sub-command
                else:
                    update.message.reply_text(
                        text="Only `add` and `remove` are supported",
                        parse_mode=ParseMode.MARKDOWN)
                    return

                # Reply with message
                if res["success"]:
                    update.message.reply_text(f"{emo.CHECK} {res['msg']}")
                else:
                    update.message.reply_text(f"{emo.ERROR} {res['msg']}")
            except Exception as e:
                update.message.reply_text(text=f"{emo.ERROR} {e}")

        else:
            update.message.reply_text(
                text=f"Unknown command `{command}`",
                parse_mode=ParseMode.MARKDOWN)
