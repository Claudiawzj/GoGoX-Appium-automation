"""Shared explicit waits; fail rather than choose an ambiguous control."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    def __init__(self, driver, wait_seconds=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_seconds,
                                  ignored_exceptions=(StaleElementReferenceException,))

    def visible_control(self, locator):
        def find_unique_visible(session):
            matches = [item for item in session.find_elements(*locator) if item.is_displayed()]
            if len(matches) > 1:
                raise ValueError(f"Locator matched multiple visible controls: {locator[1]}")
            return matches[0] if matches else False

        return self.wait.until(find_unique_visible, message=f"Control did not appear: {locator[1]}")
