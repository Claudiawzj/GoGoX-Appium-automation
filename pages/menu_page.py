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

    def account_state(self):
        logging.info("STEP: Determine whether the home menu is guest or signed in")

        def state(session):
            guests = [e for e in session.find_elements(*menu.GUEST) if e.is_displayed()]
            links = [e for e in session.find_elements(*menu.LOG_IN_OR_SIGN_UP)
                     if e.is_displayed()]
            if guests and any(e.is_enabled() for e in links):
                return "guest"
            personal = [e for e in session.find_elements(*menu.PERSONAL_ACCOUNT)
                        if e.is_displayed()]
            if personal and not guests and all(not e.is_enabled() for e in links):
                return "signed_in"
            return False

        return self.wait.until(state, message="Could not verify guest or personal-account state.")

    def close(self):
        logging.info("STEP: Close the account menu and return to Transport")
        self.visible_control(menu.YOUR_ORDERS)
        # Observed drawer leaves a backdrop at the screen's right edge.
        size = self.driver.get_window_size()
        self.driver.execute_script("mobile: tap", {
            "x": size["width"] - 12, "y": size["height"] * 0.12,
        })
        self.wait.until(lambda session: not any(e.is_displayed() for e in
                        session.find_elements(*menu.YOUR_ORDERS)),
                        message="Account menu did not close.")
        self.visible_control(home.MENU)
        return self

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
