"""Future pickup and required rental/vehicle checkpoint; ends before extras/review."""

import pytest

from pages.order_details_page import OrderDetailsPage
from pages.time_vehicle_page import TimeVehiclePage
from utils.settings import load_time_vehicle_data


@pytest.mark.device
def test_future_pickup_four_hour_van(driver, device_settings):
    plan, rental_hours, vehicle = load_time_vehicle_data()
    page = TimeVehiclePage(driver, device_settings["wait_seconds"])
    page.configure(plan, rental_hours, vehicle)
    page.assert_selections(plan)
    page.proceed(plan)
    OrderDetailsPage(driver, device_settings["wait_seconds"]).wait_for_screen()
