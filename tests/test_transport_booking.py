"""Existing-account booking practice, from restart to Review with HK$20 tip.

Logs in with saved existing credentials if signed out; does not create a new account.
"""

import logging
import pytest

from pages.home_page import HomePage
from pages.location_page import LocationPage
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.order_details_page import OrderDetailsPage
from pages.time_vehicle_page import TimeVehiclePage
from utils.settings import (ROOT, load_route_data, load_time_vehicle_data,
                            load_extras_data, load_login_credentials)


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
    account_menu = MenuPage(driver, wait).open()
    if account_menu.account_state() == "guest":
        logging.info("STEP: Guest detected; log in with the existing account before booking")
        email, password = load_login_credentials()
        account_menu.open_guest_login()
        try:
            login = LoginPage(driver, wait).enter_existing_email(email)
            login.submit_existing_password(password)
            home.wait_for_transport_screen()
        except Exception:
            # Suppress nested login frames that could include private arguments.
            raise RuntimeError("Existing-account login failed; booking was not started. "
                               "No automatic password retry was performed.") from None
        account_menu.open()
    else:
        logging.info("STEP: Existing account already signed in; no password submission needed")
    account_menu.wait_for_signed_in().close()
    home.wait_for_transport_screen()
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
