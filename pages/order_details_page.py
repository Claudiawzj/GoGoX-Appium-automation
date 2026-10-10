"""Required extras on a fresh order draft. Never implements order submission."""

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

    def _tap_right_control(self, label):
        # These custom plus/checkbox controls have no accessible identifiers.
        # Anchor the observed right-edge control to its own semantic row, not screen pixels.
        cell = self.visible_control(order_details.row(label))
        rect = cell.rect
        self.driver.execute_script("mobile: tap", {
            "x": rect["x"] + rect["width"] - 32,
            "y": rect["y"] + rect["height"] / 2,
        })

    def configure_extras(self, tunnel):
        if tunnel != "Cross-Harbour Tunnel (Hung Hom)":
            raise ValueError("Only the inspected and approved tunnel choice is supported.")
        self.wait_for_screen()
        # Do not repeat unchecked toggles on an already edited draft.
        self.visible_control(order_details.count("Passengers", 2))
        self.visible_control(order_details.count("Rent a cart", 0))
        logging.info("STEP: Select Basic $10 cargo compensation")
        self.visible_control(order_details.BASIC).click()
        logging.info("STEP: Set three passengers and rent one cart")
        self._tap_right_control("Passengers")
        self.visible_control(order_details.count("Passengers", 3))
        self._tap_right_control("Rent a cart")
        self.visible_control(order_details.count("Rent a cart", 1))
        for label in ("Premium Van", "Goods longer than 6 ft", "Pet-friendly driver",
                      "English-speaking driver"):
            logging.info("STEP: Select %s", label)
            self._tap_right_control(label)
        logging.info("STEP: Select the approved tunnel in its preference sheet")
        self._tap_right_control("Tunnel preference")
        self.visible_control(order_details.TUNNEL_EXPLANATION)
        self.visible_control(order_details.TUNNEL_CHOICE).click()
        # This Confirm belongs to the tunnel sheet, not an order confirmation.
        self.visible_control(order_details.TUNNEL_CONFIRM).click()
        self.visible_control(order_details.TITLE)
        self.visible_control(order_details.TUNNEL_CHOICE)
        logging.info("STEP: Scroll to Move door-to-door and select it")
        self.driver.execute_script("mobile: swipe", {"direction": "up"})
        self._tap_right_control("Move door-to-door")
        return self

    def open_review(self):
        self.visible_control(order_details.TITLE)
        logging.info("STEP: Open Review from Order details; never submit an order")
        self.visible_control(order_details.REVIEW).click()
        from pages.review_page import ReviewPage
        return ReviewPage(self.driver, self.wait_seconds).wait_for_screen()
