"""Repeatable existing-account login checkpoint; not the full assignment flow."""

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from utils.settings import load_login_credentials


@pytest.mark.device
def test_existing_email_login(driver, device_settings):
    email, password = load_login_credentials()
    wait_seconds = device_settings["wait_seconds"]
    home = HomePage(driver, wait_seconds).wait_for_empty_transport_screen()
    menu = MenuPage(driver, wait_seconds).open()
    menu.open_guest_login()
    login = LoginPage(driver, wait_seconds).enter_existing_email(email)
    login.submit_existing_password(password)
    home.wait_for_empty_transport_screen()
    assert home.transport_is_selected(), "Transport should be selected after login."
    menu.open().wait_for_signed_in()
