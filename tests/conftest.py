"""A device session is opt-in until signing and configuration are ready."""

import logging

import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions

from utils.settings import load_device_settings


def pytest_addoption(parser):
    parser.addoption("--device", action="store_true", help="Run tests on the connected iPhone")
    parser.addoption("--register", action="store_true",
                     help="Create the configured new account in the full booking test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--register"):
        expected = "tests/test_transport_booking.py::test_transport_to_review_with_twenty_dollar_tip"
        if not config.getoption("--device") or len(items) != 1 or items[0].nodeid != expected:
            raise pytest.UsageError("--register requires --device and only "
                                    "tests/test_transport_booking.py. No test was run.")


@pytest.fixture
def device_settings(request):
    if not request.config.getoption("--device"):
        pytest.skip("Device run not requested; use --device after setup is complete.")
    return load_device_settings()


@pytest.fixture
def driver(device_settings, request):
    capabilities = dict(device_settings["capabilities"])
    if request.node.get_closest_marker("restart_app"):
        # This test owns the app restart. Avoid launching here and again in the test.
        capabilities["appium:autoLaunch"] = False
        logging.info("STEP: Connect to the iPhone; the booking test will launch GoGoX once")
    else:
        logging.info("STEP: Connect to the iPhone and launch the configured GoGoX app")
    options = XCUITestOptions().load_capabilities(capabilities)
    session = webdriver.Remote(device_settings["server_url"], options=options)
    session.implicitly_wait(0)
    try:
        yield session
    finally:
        logging.info("STEP: End the automation session")
        session.quit()
