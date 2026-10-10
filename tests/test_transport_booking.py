"""Existing-account booking practice, from restart to Review with HK$20 tip.

Registration/login are separate checkpoints; this test does not satisfy fresh signup.
"""

import logging
import pytest

from pages.home_page import HomePage
from pages.location_page import LocationPage
from pages.order_details_page import OrderDetailsPage
from pages.time_vehicle_page import TimeVehiclePage
from utils.settings import ROOT, load_route_data, load_time_vehicle_data, load_extras_data


@pytest.mark.device
def test_transport_to_review_with_twenty_dollar_tip(driver, device_settings):
    route = load_route_data()
    plan, hours, vehicle = load_time_vehicle_data()
    tunnel, contact = load_extras_data()
    wait = device_settings["wait_seconds"]
    bundle = device_settings["capabilities"]["appium:bundleId"]
    logging.info("STEP: Restart GoGoX, preserving the existing account")
    driver.terminate_app(bundle)
    driver.activate_app(bundle)
    home = HomePage(driver, wait).wait_for_transport_screen()
    assert home.transport_is_selected(), "Transport must be the selected service."
    locations = LocationPage(driver, wait)
    home.open_pickup()
    locations.choose_pickup(route["from_location"], route["from_result"])
    home.open_destination()
    locations.choose_destination(route["to_location"], route["to_result"])
    home.wait_for_route(route["from_result"], route["to_result"])
    home.next_from_route()
    timing = TimeVehiclePage(driver, wait).wait_for_screen()
    timing.configure(plan, hours, vehicle)
    timing.proceed(plan)
    details = OrderDetailsPage(driver, wait).wait_for_screen()
    details.configure_extras(tunnel)
    review = details.open_review()
    review.verify_route_and_pickup(route, plan)
    review.save_dummy_contact(contact)
    review.add_twenty_dollar_tip()
    review.assert_required_summary()
    output = ROOT / "reports" / "transport-booking-final.png"
    driver.save_screenshot(str(output))
    output.chmod(0o600)
    logging.info("STEP: Stop at Review with HK$20 tip; no order-submission action exists")
