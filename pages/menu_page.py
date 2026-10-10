"""Menu navigation and signed-in checkpoint; no account or order creation."""

import logging

from pages.base_page import BasePage
from pages.locators import home, menu


class MenuPage(BasePage):
    def open(self):
        logging.info("STEP: Open the home menu")
        self.visible_control(home.MENU).click()
        self.visible_control(menu.YOUR_ORDERS)
        return self

    def open_guest_login(self):
        logging.info("STEP: Check the guest state and open email login")
        self.visible_control(menu.GUEST)
        self.visible_control(menu.LOG_IN_OR_SIGN_UP).click()

    def wait_for_signed_in(self):
        logging.info("STEP: Confirm the personal-account menu and disabled sign-in control")
        self.visible_control(menu.YOUR_ORDERS)
        self.visible_control(menu.PERSONAL_ACCOUNT)
        self.visible_control(menu.PERSONAL)
        # The app retains the sign-in accessibility ID after login, but disables
        # it and removes its label. Its absence is not a valid success condition.
        self.wait.until(
            lambda session: not session.find_elements(*menu.GUEST)
            and all(not item.is_enabled()
                    for item in session.find_elements(*menu.LOG_IN_OR_SIGN_UP)),
            message="The personal menu still has an active guest/sign-in control.",
        )
        return self
