import logging
import requests
import idena.emoji as emo

from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Check(IdenaPlugin):

    def __enter__(self):
        self.config.set(False, "job_running")

        if self.config.get("job_autostart"):
            # Start job to check if node is still mining
            interval = self.config.get("job_interval")
            self.repeat_job(self._node_check, interval)

            # Save info that node check is active
            self.config.set(True, "job_running")
        return self

    @IdenaPlugin.owner
    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if len(args) > 0:
            argument = args[0].lower()

            if argument == "on":
                if self.config.get("job_running"):
                    msg = f"{emo.INFO} Node check already active"
                    update.message.reply_text(msg)
                    return

                # Start job to check if node is still mining
                interval = self.config.get("job_interval")
                self.repeat_job(self._node_check, interval)

                # Save info that node check is active
                self.config.set(True, "job_running")

                msg = f"{emo.CHECK} Node check activated"
                update.message.reply_text(msg)

            elif argument == "off":
                if not self.config.get("job_running"):
                    msg = f"{emo.INFO} Node check already deactivated"
                    update.message.reply_text(msg)
                    return

                # Stop job to check if node is still mining
                job = self.get_job(self.get_name())
                if job: job.schedule_removal()

                # Save info that node check if deactivated
                self.config.set(False, "job_running")

                msg = f"{emo.CHECK} Node check deactivated"
                update.message.reply_text(msg)

        else:
            address = self.api().address()

            if "error" in address:
                error = address["error"]["message"]
                msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                logging.error(msg)
                return

            result = self.check_online(address['result'])

            if result["success"]:
                if result["message"]:
                    msg = result["message"]
                else:
                    msg = f"Mining Status: `{result['mining']}`\n" \
                          f"Last Seen: `{result['last_seen']}`"
            else:
                msg = f"{emo.ERROR} {result['message']}"

            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

    def _node_check(self, bot, job):
        address = self.api().address()

        if "error" in address:
            error = address["error"]["message"]
            msg = f"{emo.ERROR} Couldn't retrieve address: {error}"
            logging.error(msg)
            return

        result = self.check_online(address['result'])

        if not result["success"]:
            job.schedule_removal()
            self.config.set(False, "job_running")
            msg = f"{emo.CANCEL} Can't watch node"

        elif not result["online"]:
            last_seen = result["last_seen"]
            msg = f"{emo.ALERT} *Node is not mining!*\nLast seen: {last_seen}"

        else:
            return

        # Send notification to admins
        for admin in self.global_config.get("admin", "ids"):
            try:
                bot.send_message(admin, msg, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                msg = f"Couldn't send notification that node is not mining to ID {str(admin)}: {e}"
                logging.warning(msg)

    def check_online(self, address):
        api_url = self.config.get("api_url")
        api_url = f"{api_url}{address}"

        result = {
            "success": None,
            "message": None,
            "online": None,
            "last_seen": None
        }

        try:
            # Read IDENA explorer API to know when node was last seen
            response = requests.get(api_url, timeout=self.config.get("api_timeout")).json()
        except Exception as e:
            msg = f"{address} Could not reach API: {e}"
            logging.error(msg)

            result["success"] = False
            result["message"] = msg
            return result

        # If no last seen date-time, stop to watch node
        if not response or not response["result"] or not response["result"]["lastActivity"]:
            msg = "No 'Last Seen' date. Can not watch node"
            logging.error(f"{address} {msg}")

            result["success"] = False
            result["message"] = msg
            return result

        result["success"] = True
        result["online"] = response["result"]["online"]
        result["last_seen"] = response["result"]["lastActivity"]

        return result
