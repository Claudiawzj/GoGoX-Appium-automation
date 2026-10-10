"""Read local capabilities without exposing their contents in the report."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_device_settings():
    path = ROOT / "config" / "device.local.yaml"
    if not path.is_file():
        raise ValueError("Create config/device.local.yaml from device.example.yaml first.")
    settings = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(settings, dict) or not isinstance(settings.get("capabilities"), dict):
        raise ValueError("Local device configuration must contain a capabilities mapping.")
    required = (
        "appium:udid", "appium:bundleId", "appium:xcodeOrgId", "appium:updatedWDABundleId"
    )
    missing = [key for key in required if not settings["capabilities"].get(key)]
    if missing:
        raise ValueError("Fill these configuration fields: " + ", ".join(missing))
    return settings


def _load_private_test_data():
    path = ROOT / "config" / "data.local.yaml"
    if not path.is_file():
        raise ValueError("Create config/data.local.yaml from data.example.yaml first.")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        raise ValueError("Local test data is not valid YAML; check the file locally.") from None
    if not isinstance(data, dict):
        raise ValueError("Local test data must contain a YAML mapping.")
    return data


def load_login_credentials():
    """Read only existing-account data; errors never include credential values."""
    login = _load_private_test_data().get("login")
    if not isinstance(login, dict) or login.get("method") != "email":
        raise ValueError("Local test data needs a login section with method: email.")
    if any(not isinstance(login.get(key), str) or not login[key].strip()
           for key in ("email", "password")):
        raise ValueError("Fill both email and password in the local login section.")
    return login["email"], login["password"]


def load_route_data():
    """Load queries and exact observed results; never choose the first fuzzy match."""
    booking = _load_private_test_data().get("booking")
    if not isinstance(booking, dict):
        raise ValueError("Fill the booking section of the local test data.")
    required = ("from_location", "to_location", "from_result", "to_result")
    if any(not isinstance(booking.get(key), str) or not booking[key].strip()
           for key in required):
        raise ValueError("Fill route queries and exact results in the booking section.")
    return {key: booking[key] for key in required}
