"""Sign out of the verified Personal account to demonstrate a separate login."""

import logging

from pages.base_page import BasePage
from pages.locators import account


class AccountPage(BasePage):
    def sign_out_from_menu(self):
        logging.info("STEP: Sign out of the newly created Personal account before login")
        self.visible_control(account.SETTINGS).click()
        self.visible_control(account.SETTINGS)
        self.visible_control(account.PERSONAL).click()
        self.visible_control(account.PROFILE)
        self.visible_control(account.LOG_OUT).click()
        self.visible_control(account.SETTINGS)
        self.visible_control(account.CLOSE).click()
