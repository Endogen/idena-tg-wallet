import os
import idena.emoji as emo
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import ParseMode
from idena.plugin import IdenaPlugin


class Mining(IdenaPlugin):

    _URL = "https://scan.idena.io/identity?identity="

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

        options = Options()
        options.add_argument("--headless")
        options.binary_location = self.config.get("chrome_path")

        path = os.path.join(self.get_res_path(plugin=self.get_name()), "chromedriver")

        driver = None

        try:
            driver = webdriver.Chrome(executable_path=path, chrome_options=options)
            driver.get(f"{self._URL}{address}")

            mining = driver.find_element_by_id("OnlineMinerStatus").text
            last_seen = driver.find_element_by_id("LastSeen").text
        except Exception as e:
            msg = f"{emo.ERROR} Not possible to read 'Last Seen' date: {e}"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            logging.error(msg)
            return
        finally:
            if driver:
                driver.close()

        if mining:
            msg = f"Mining Status: `{mining}`\n" \
                  f"Last Seen: `{last_seen}`"
        else:
            msg = f"{emo.CANCEL} Mining not possible"

        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
