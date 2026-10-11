"""Create the configured account once, using the supplied Hong Kong signup form."""

import logging

from pages.login_page import LoginPage
from pages.locators import auth, registration


class RegistrationPage(LoginPage):
    def enter_unused_email(self, email):
        logging.info("STEP: Enter the unused email from private registration data")
        self._type_private(auth.EMAIL, email)
        self.visible_control(auth.EMAIL_NEXT).click()
        logging.info("STEP: Verify the signup title, password field and Sign up control")
        # An already registered address leads to login, not this title. Never
        # treat that as successful registration or silently reuse the account.
        self.visible_control(registration.TITLE)
        self.visible_control(registration.PASSWORD)
        self.visible_control(registration.SIGN_UP)
        return self

    def submit_new_password(self, password):
        logging.info("STEP: Fill the signup password; leave optional name blank")
        self.visible_control(registration.TITLE)
        self._type_private(registration.PASSWORD, password)
        # Both checkboxes are already selected in the user's screenshot. Leave
        # that state untouched; no speculative checkbox/consent taps.
        button = self.visible_control(registration.SIGN_UP)
        self.wait.until(lambda session: button.is_enabled(),
                        message="The signup button did not become enabled.")
        logging.info("STEP: Submit Sign up once; no automatic signup retry")
        button.click()
