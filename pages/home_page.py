"""Transport home checks and route editing. No order-submission action."""

import logging

from pages.base_page import BasePage
from pages.locators import home


class HomePage(BasePage):
    def wait_for_transport_screen(self, dismiss_promotion=False):
        controls = (home.MENU, home.TRANSPORT, home.FROM_FIELD, home.TO_FIELD, home.NEXT)
        if dismiss_promotion:
            def ready(session):
                closes = [e for e in session.find_elements(*home.PROMOTION_CLOSE)
                          if e.is_displayed()]
                if len(closes) > 1:
                    raise ValueError("Multiple promotion close controls are visible.")
                if closes:
                    logging.info("STEP: Close the observed promotion overlay to reach Transport")
                    closes[0].click()
                    return False
                for locator in controls:
                    matches = [e for e in session.find_elements(*locator) if e.is_displayed()]
                    if len(matches) > 1:
                        raise ValueError("A Transport control matched multiple visible elements.")
                    if not matches:
                        return False
                return True

            self.wait.until(ready, message="Transport controls did not appear after promotion handling.")
        else:
            for locator in controls:
                self.visible_control(locator)
        return self

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

    def open_pickup(self):
        logging.info("STEP: Open the pickup location editor")
        self.visible_control(home.FROM_FIELD).click()

    def open_destination(self):
        logging.info("STEP: Open the destination location editor")
        self.visible_control(home.TO_FIELD).click()

    def route_values(self):
        return (self.visible_control(home.FROM_FIELD).get_attribute("value") or "",
                self.visible_control(home.TO_FIELD).get_attribute("value") or "")

    def wait_for_route(self, pickup, destination):
        logging.info("STEP: Verify the saved pickup and destination addresses")
        self.wait_for_transport_screen()
        self.wait.until(lambda session: self.route_values() == (pickup, destination),
                        message="Home route fields do not match the selected addresses.")
        return self

    def next_from_route(self):
        logging.info("STEP: Proceed from the verified route to booking details")
        self.visible_control(home.NEXT).click()
