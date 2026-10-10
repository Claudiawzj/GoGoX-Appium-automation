"""Read-only endpoint of the time/vehicle checkpoint. No review/submission action."""

import logging

from pages.base_page import BasePage
from pages.locators import order_details


class OrderDetailsPage(BasePage):
    def wait_for_screen(self):
        logging.info("STEP: Confirm Order details and Cargo compensation are visible")
        self.visible_control(order_details.TITLE)
        self.visible_control(order_details.COMPENSATION)
        self.visible_control(order_details.BASIC)
        return self
