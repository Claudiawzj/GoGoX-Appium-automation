"""Read-only Home Page checks; no booking or submission action."""

import logging

from pages.base_page import BasePage
from pages.locators import home


class HomePage(BasePage):
    def wait_for_empty_transport_screen(self):
        logging.info("STEP: Wait for the Transport home screen and its route controls")
        self.visible_control(home.MENU)
        self.visible_control(home.TRANSPORT)
        self.visible_control(home.FROM)
        self.visible_control(home.TO)
        self.visible_control(home.NEXT)
        return self

    def transport_is_selected(self):
        return self.visible_control(home.TRANSPORT).get_attribute("value") == "1"

    def route_placeholders(self):
        return (
            self.visible_control(home.FROM).get_attribute("label"),
            self.visible_control(home.TO).get_attribute("label"),
        )
