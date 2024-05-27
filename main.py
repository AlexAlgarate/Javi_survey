import time
from typing import Any, Dict, Tuple, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

seconds = 5
URL = "https://encuesta.com/survey/VZr4mTd8XQ/hotario-verano"

survery_elements: Dict[
    str,
    Tuple[Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str],
] = {
    "click_radio_button": (
        EC.element_to_be_clickable,
        By.CLASS_NAME,
        "v-input--selection-controls__ripple",
    ),
    "accept_survey": (
        EC.element_to_be_clickable,
        By.CLASS_NAME,
        "ee__button--next",
    ),
}


def find_element(
    driver, condition: EC, locator: By, selector: str, element_to_wait_for: Any = None
) -> WebElement:
    try:
        wait = WebDriverWait(
            driver=element_to_wait_for if element_to_wait_for is not None else driver,
            timeout=seconds,
        )
        element = wait.until(condition((locator, selector)))
        return element

    except TimeoutException:
        print(f"TimeoutException: Element not found with {locator} = {selector} within the expected time.")
        return None
    except NoSuchElementException:
        print(f"NoSuchElementException: Element not found with {locator} = {selector}.")
        return None


def click_button(element: WebElement) -> None:
    if element:
        element.click()
    else:
        print("Could not click on the element")


def setup_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=Service(), options=options)


def click_radio_button(driver) -> bool:
    radio_button = find_element(driver, *survery_elements["click_radio_button"])
    click_button(radio_button)
    time.sleep(1)
    return True


def click_finish(driver) -> bool:
    accept_survey = find_element(driver, *survery_elements["accept_survey"])
    click_button(accept_survey)
    time.sleep(2)
    return True


def main():
    try:
        with setup_driver() as driver:
            driver.implicitly_wait(time_to_wait=seconds)
            driver.get(URL)
            click_radio_button(driver)
            click_finish(driver)
            driver.quit()
    except Exception as e:
        raise Exception(f"Exception: {e}")


if __name__ == "__main__":
    try:
        i = 1
        while True:
            main()
            print(f"main() function called {i} times")
            i += 1
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
