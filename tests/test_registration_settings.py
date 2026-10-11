"""Offline checks: signup must not consume the existing account's credentials."""

import pytest

from utils import settings


def test_registration_reads_its_own_credentials(monkeypatch):
    data = {"login": {"method": "email", "email": "existing@example.invalid", "password": "old-secret"},
            "registration": {"method": "email", "email": "new@example.invalid",
                             "password": "new-secret"}}
    monkeypatch.setattr(settings, "_load_private_test_data", lambda: data)
    assert settings.load_registration_credentials() == ("new@example.invalid", "new-secret")
    assert settings.load_login_credentials() == ("existing@example.invalid", "old-secret")


@pytest.mark.parametrize("registration", [None, {"method": "phone"},
    {"method": "email", "email": "", "password": "new-secret"},
    {"method": "email", "email": "new@example.invalid", "password": ""}])
def test_missing_signup_data_never_falls_back_to_login(monkeypatch, registration):
    monkeypatch.setattr(settings, "_load_private_test_data", lambda: {
        "login": {"email": "existing@example.invalid", "password": "old-secret"},
        "registration": registration})
    with pytest.raises(ValueError) as error:
        settings.load_registration_credentials()
    assert "old-secret" not in str(error.value)
    assert "existing@example.invalid" not in str(error.value)


def test_same_existing_address_is_rejected_ignoring_case_and_spacing(monkeypatch):
    monkeypatch.setattr(settings, "_load_private_test_data", lambda: {
        "login": {"email": "existing@example.invalid"},
        "registration": {"method": "email", "email": " Existing@example.invalid ",
                         "password": "new-secret"}})
    with pytest.raises(ValueError, match="different, unused email"):
        settings.load_registration_credentials()
