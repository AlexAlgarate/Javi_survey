import logging
import time
from typing import Any, Dict, Tuple, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import config as config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SurveyBot:
    def __init__(
        self,
        url: str,
        web_elements: Dict[
            str,
            Tuple[
                Union[EC.visibility_of_element_located, EC.element_to_be_clickable],
                By,
                str,
            ],
        ],
    ):
        self.url = url
        self.wait_time: int = 5
        self.driver = self.setup_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.web_elements = web_elements

    def setup_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        arguments = ["--start-maximized", "--disable-gpu", "--disable-extensions"]
        for args in arguments:
            options.add_argument(args)
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(service=Service(), options=options)

    def _find_element(
        self,
        condition: EC,
        locator: By,
        selector: str,
        element_to_wait_for: Any = None,
    ) -> WebElement:
        try:
            wait = WebDriverWait(
                driver=(element_to_wait_for if element_to_wait_for is not None else self.driver),
                timeout=self.wait_time,
            )
            element = wait.until(condition((locator, selector)))
            return element
        except TimeoutException:
            logging.error(
                f"TimeoutException: Element not found with {locator} = {selector} within the expected time."
            )
            return None
        except NoSuchElementException:
            logging.error(f"NoSuchElementException: Element not found with {locator} = {selector}.")
            return None

    def _click_button(self, element: WebElement) -> None:
        if element:
            try:
                element.click()
            except Exception as e:
                logging.error(f"Exception occurred while clicking the element: {e}")
        else:
            logging.error("Could not click on the element")

    def click_cookies(self, element: str) -> bool:
        radio_button = self._find_element(*self.web_elements[element])
        self._click_button(radio_button)
        time.sleep(1)
        return True

    def click_login(self, element: str) -> bool:
        accept_survey = self._find_element(*self.web_elements[element])
        self._click_button(accept_survey)
        time.sleep(5)
        return True

    def run(self, cookies: str, login: str):
        self.driver.implicitly_wait(time_to_wait=self.wait_time)
        try:
            self.driver.get(self.url)
            self.click_cookies(cookies)
            self.click_login(login)
            print("Login button clicked.")
        finally:
            self.driver.quit()


def main():
    bot = SurveyBot(config.URL, config.web_elements)
    bot.run("accept_cookie", "login_button")


if __name__ == "__main__":
    main()
