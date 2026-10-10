"""Future pickup, four-hour rental and Van selection; no order submission."""

import logging
from datetime import datetime

from pages.base_page import BasePage
from pages.locators import pickers, time_vehicle
from pages.pickup_page import PickupPage
from utils.pickup_plan import HONG_KONG, normalize_label


class TimeVehiclePage(BasePage):
    def wait_for_screen(self):
        logging.info("STEP: Confirm the Time and vehicle screen after the route")
        self.visible_control(time_vehicle.TITLE)
        self.visible_control(time_vehicle.HOURLY_RENTAL)
        self.visible_control(time_vehicle.VAN)
        return self

    def configure(self, plan, rental_hours, vehicle):
        if rental_hours != 4 or vehicle != "Van":
            raise ValueError("The assignment requires four-hour rental and Van.")
        self.wait_for_screen()
        self.visible_control(time_vehicle.CALENDAR).click()
        PickupPage(self.driver, self.wait_seconds).select(plan)
        self.wait.until(lambda session: self.pickup_summary() == plan.summary_label,
                        message="Saved pickup summary does not match the future plan.")
        logging.info("STEP: Select four-hour hourly rental")
        self.visible_control(time_vehicle.HOURLY_RENTAL).click()

        def rental_wheel(session):
            wheels = [item for item in session.find_elements(*pickers.WHEELS)
                      if item.is_displayed()]
            return wheels[0] if len(wheels) == 1 else False

        wheel = self.wait.until(rental_wheel, message="Rental sheet needs one visible wheel.")
        wheel.send_keys("4 hours")
        self.wait.until(lambda session: rental_wheel(session)
                        and normalize_label(rental_wheel(session).get_attribute("value")) == "4 hours",
                        message="Rental wheel did not select four hours.")
        self.visible_control(pickers.OK).click()
        self.wait.until(lambda session: not session.find_elements(*pickers.WHEELS))
        self.visible_control(time_vehicle.FOUR_HOURS)
        self.select_van()
        return self

    def select_van(self):
        logging.info("STEP: Wait for the Van card to settle, tap its whole card and verify selection")
        previous_rect = None

        def settled_card(session):
            nonlocal previous_rect
            cards = [e for e in session.find_elements(*time_vehicle.VAN_CARD)
                     if e.is_displayed()]
            if len(cards) != 1:
                previous_rect = None
                return False
            card = cards[0]
            rect = card.rect
            settled = rect == previous_rect and rect["height"] > 0
            previous_rect = rect
            return card if settled else False

        # Rental-sheet dismissal can reflow the vehicle table. Use the full semantic
        # card only after consecutive observations agree, rather than its moving label.
        self.wait.until(settled_card, message="Van card did not settle after rental selection.").click()
        self.visible_control(time_vehicle.VAN_SELECTED)
        return self

    def pickup_summary(self):
        return normalize_label(self.visible_control(time_vehicle.PICKUP_SUMMARY)
                               .get_attribute("label"))

    def assert_selections(self, plan):
        logging.info("STEP: Verify saved future pickup, four-hour rental and Van")
        self.wait_for_screen()
        assert plan.scheduled_at > datetime.now(HONG_KONG), "Pickup must remain in the future."
        assert self.pickup_summary() == plan.summary_label, "Saved date/time differs from the plan."
        assert self.visible_control(time_vehicle.FOUR_HOURS).get_attribute("label") == "4 hours"
        assert self.visible_control(time_vehicle.VAN_SELECTED).is_displayed(), "Van must be selected."

    def proceed(self, plan):
        # Scope the shared footer strictly to this verified page, never a review page.
        self.assert_selections(plan)
        logging.info("STEP: Tap Next from verified time/vehicle settings")
        self.visible_control(time_vehicle.NEXT).click()
