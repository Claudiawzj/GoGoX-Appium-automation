"""Select future pickup date/time with native wheels and explicit verification."""

import logging
from datetime import datetime

from pages.base_page import BasePage
from pages.locators import pickers
from utils.pickup_plan import HONG_KONG, normalize_label


class PickupPage(BasePage):
    def _wheels(self):
        return self.wait.until(
            lambda session: self._visible_wheels(session),
            message="Pickup sheet must contain exactly two visible wheels.")

    @staticmethod
    def _visible_wheels(session):
        wheels = [item for item in session.find_elements(*pickers.WHEELS)
                  if item.is_displayed()]
        return wheels if len(wheels) == 2 else False

    def select(self, plan):
        if plan.scheduled_at <= datetime.now(HONG_KONG):
            raise ValueError("The pickup plan is no longer in the future.")
        logging.info("STEP: Set future pickup to %s", plan.scheduled_at.isoformat())
        self.visible_control(pickers.PICKUP_TITLE)
        self._wheels()[0].send_keys(plan.date_label)

        def date_matches(session):
            wheels = self._visible_wheels(session)
            return wheels and normalize_label(wheels[0].get_attribute("value")) == plan.date_label

        self.wait.until(date_matches,
                        message="Pickup date wheel did not reach the future date.")
        # Exact locale typography is required for iOS to select the intended slot.
        native_time = plan.time_label.replace(" am ", "\u202fam ").replace(" pm ", "\u202fpm ")
        self._wheels()[1].send_keys(native_time)

        def values_match(session):
            wheels = self._visible_wheels(session)
            return wheels and (
                normalize_label(wheels[0].get_attribute("value")) == plan.date_label
                and normalize_label(wheels[1].get_attribute("value")) == plan.time_label)

        self.wait.until(values_match, message="Pickup wheel date/time does not match the plan.")
        self.visible_control(pickers.OK).click()
        self.wait.until(lambda session: not session.find_elements(*pickers.WHEELS),
                        message="Pickup sheet did not close after confirmation.")
