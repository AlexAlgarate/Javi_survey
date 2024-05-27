from typing import Dict, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.eldiario.es/"
web_elements: Dict[
    str,
    Tuple[Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str],
] = {
    "accept_cookie": (
        EC.element_to_be_clickable,
        By.ID,
        "didomi-notice-agree-button",
    ),
    "login_button": (
        EC.element_to_be_clickable,
        By.CLASS_NAME,
        "login",
    ),
}
