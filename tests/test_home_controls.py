"""Verify real home-screen locators without tapping or entering account data."""

import logging

import pytest

from pages.home_page import HomePage


@pytest.mark.device
def test_empty_transport_home_controls(driver, device_settings):
    page = HomePage(driver, device_settings["wait_seconds"])
    page.wait_for_empty_transport_screen()
    assert page.transport_is_selected(), "The Transport service must be selected."
    assert page.route_placeholders() == ("Where from?", "Where to?"), (
        "This initial locator check requires an empty From/To route."
    )
    logging.info("CHECKPOINT: Transport and empty route controls verified; no taps performed")
