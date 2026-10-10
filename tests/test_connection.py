"""First milestone: launch GoGoX and confirm it is in the foreground.

This test makes no taps, enters no account details and creates no booking.
"""

import logging

import pytest
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.device
def test_gogox_opens_on_iphone(driver, device_settings):
    bundle_id = device_settings["capabilities"]["appium:bundleId"]
    logging.info("STEP: Wait for GoGoX to be running in the foreground")
    WebDriverWait(driver, device_settings["wait_seconds"]).until(
        lambda session: session.query_app_state(bundle_id) == 4,
        message="The configured GoGoX app did not enter the foreground.",
    )
    assert driver.query_app_state(bundle_id) == 4, "GoGoX must be running in the foreground."
    logging.info("CHECKPOINT: App launch verified; no booking actions performed")
