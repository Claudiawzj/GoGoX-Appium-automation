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
