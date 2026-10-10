"""Initial read-only checkpoint; future time and rental actions are still pending."""

import logging

from pages.base_page import BasePage
from pages.locators import time_vehicle


class TimeVehiclePage(BasePage):
    def wait_for_screen(self):
        logging.info("STEP: Confirm the Time and vehicle screen after the route")
        self.visible_control(time_vehicle.TITLE)
        self.visible_control(time_vehicle.HOURLY_RENTAL)
        self.visible_control(time_vehicle.VAN)
        return self
