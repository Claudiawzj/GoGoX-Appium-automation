"""Existing-account login only. No registration action or automatic login retry."""

import logging

from selenium.common.exceptions import WebDriverException

from pages.base_page import BasePage
from pages.locators import auth


class LoginPage(BasePage):
    def _type_private(self, locator, text):
        # The app exposes inputs as Other elements, not native TextField elements.
        field = self.visible_control(locator)
        field.click()
        self.wait.until(lambda session: session.is_keyboard_shown(),
                        message="The keyboard did not appear for the login field.")
        try:
            field.send_keys(text)
        except WebDriverException:
            # Driver exceptions can contain submitted text; keep it out of reports.
            raise RuntimeError("Could not type into the private login field.") from None

    def enter_existing_email(self, email):
        logging.info("STEP: Enter the existing-account email from private local data")
        self._type_private(auth.EMAIL, email)
        self.visible_control(auth.EMAIL_NEXT).click()
        # A registered email must lead to the password-login screen. Never accept
        # the registration screen as an alternative or submit registration data.
        self.visible_control(auth.PASSWORD_TITLE)
        self.visible_control(auth.PASSWORD)
        self.visible_control(auth.LOG_IN)
        return self

    def submit_existing_password(self, password):
        logging.info("STEP: Enter the private password and submit login once")
        self.visible_control(auth.PASSWORD_TITLE)
        self._type_private(auth.PASSWORD, password)
        self.visible_control(auth.LOG_IN).click()
