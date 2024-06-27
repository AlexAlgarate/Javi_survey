import unittest
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from main_oop import SurveyBot


class TestSurveyBot(unittest.TestCase):
    @patch("selenium.webdriver.Chrome")
    def setUp(self, MockChrome):
        self.mock_driver = MockChrome.return_value
        self.mock_driver.find_element.return_value = MagicMock()
        self.mock_wait = patch("selenium.webdriver.support.wait.WebDriverWait").start()
        self.addCleanup(patch.stopall)

        self.web_elements = {
            "accept_cookie": (EC.element_to_be_clickable, By.ID, "accept-cookies"),
            "login_button": (EC.element_to_be_clickable, By.ID, "login"),
        }
        self.bot = SurveyBot("http://example.com", self.web_elements)

    def test_find_element_success(self):
        condition = EC.element_to_be_clickable
        self.mock_wait().until.return_value = self.mock_driver.find_element

        element = self.bot._find_element(condition, By.ID, "accept-cookies")
        self.assertIsNone(element)

    def test_find_element_timeout_exception(self):
        condition = EC.element_to_be_clickable
        self.mock_wait().until.side_effect = TimeoutException

        element = self.bot._find_element(condition, By.ID, "accept-cookies")
        self.assertIsNone(element)

    def test_find_element_no_such_element_exception(self):
        condition = EC.element_to_be_clickable
        self.mock_wait().until.side_effect = NoSuchElementException

        element = self.bot._find_element(condition, By.ID, "accept-cookies")
        self.assertIsNone(element)

    def test_click_element_success(self):
        element = MagicMock()
        self.bot._click_element(element)
        element.click.assert_called_once()

    def test_click_element_failure(self):
        element = None
        with self.assertLogs(level="ERROR") as log:
            self.bot._click_element(element)
            self.assertIn("Could not click on the element", log.output[0])

    def test_click_action(self):
        self.mock_wait().until.return_value = self.mock_driver.find_element
        result = self.bot._click_action("accept_cookie")
        self.assertTrue(result)

    def test_accept_cookies(self):
        self.mock_wait().until.return_value = self.mock_driver.find_element
        result = self.bot.accept_cookies("accept_cookie")
        self.assertTrue(result)

    def test_click_login(self):
        self.mock_wait().until.return_value = self.mock_driver.find_element
        result = self.bot.click_login("login_button")
        self.assertTrue(result)

    def test_run(self):
        with patch.object(
            self.bot, "accept_cookies", return_value=True
        ) as mock_accept_cookies, patch.object(
            self.bot, "click_login", return_value=True
        ) as mock_click_login:
            self.bot.run("accept_cookie", "login_button")
            mock_accept_cookies.assert_called_once_with("accept_cookie")
            mock_click_login.assert_called_once_with("login_button")


if __name__ == "__main__":
    unittest.main()
