"""Signed-in route checkpoint. Ends at Time and vehicle without submitting an order."""

import logging

import pytest

from pages.home_page import HomePage
from pages.location_page import LocationPage
from pages.time_vehicle_page import TimeVehiclePage
from utils.settings import load_route_data


@pytest.mark.device
def test_configured_transport_route(driver, device_settings):
    route = load_route_data()
    wait_seconds = device_settings["wait_seconds"]
    home = HomePage(driver, wait_seconds).wait_for_transport_screen()
    assert home.transport_is_selected(), "Route test requires the Transport service."
    logging.info("STEP: Replace both home route fields with the approved practice route")
    locations = LocationPage(driver, wait_seconds)
    home.open_pickup()
    locations.choose_pickup(route["from_location"], route["from_result"])
    home.open_destination()
    locations.choose_destination(route["to_location"], route["to_result"])
    home.wait_for_route(route["from_result"], route["to_result"])
    assert home.route_values() == (route["from_result"], route["to_result"])
    home.next_from_route()
    TimeVehiclePage(driver, wait_seconds).wait_for_screen()
