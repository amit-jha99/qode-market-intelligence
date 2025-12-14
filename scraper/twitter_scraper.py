# Selenium scraper implementation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from collections import deque
import time
import logging


HASHTAGS = ["#nifty50", "#sensex", "#intraday", "#banknifty"]


class TwitterScraper:
    def __init__(self, driver):
        self.driver = driver
        self.tweets = deque(maxlen=5000)

    def scrape(self):
        for tag in HASHTAGS:
            self.driver.get(f"https://twitter.com/search?q={tag}&f=live")
            time.sleep(5)
            self._scroll_and_collect()

    def _scroll_and_collect(self):
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )

        while len(self.tweets) < 2000:
            cards = self.driver.find_elements(By.XPATH, "//article")

            for card in cards:
                tweet = self._parse_card(card)
                if tweet:
                    self.tweets.append(tweet)

            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break

            last_height = new_height

    def _parse_card(self, card):
        try:
            text = card.text
            return {
                "content": text,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logging.error(e)
            return None
