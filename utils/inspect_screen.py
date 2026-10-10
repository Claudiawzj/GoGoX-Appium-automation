"""Capture the actual GoGoX screen without tapping or entering data.

Run from the project directory: .venv/bin/python -m utils.inspect_screen
The XML and screenshot stay in the ignored reports directory because they may
contain personal information. Inspect them before sharing.
"""

import logging
from pathlib import Path
from xml.etree import ElementTree

from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from utils.settings import ROOT, load_device_settings


def interactive_screen(session):
    """Wait for visible controls instead of capturing a transient splash screen."""
    source = session.page_source
    tree = ElementTree.fromstring(source)
    kinds = {"XCUIElementTypeButton", "XCUIElementTypeTextField", "XCUIElementTypeSecureTextField"}
    if any(node.get("type") in kinds and node.get("visible") == "true" for node in tree.iter()):
        return source
    return False


def capture_screen():
    settings = load_device_settings()
    output = ROOT / "reports" / "inspection"
    output.mkdir(parents=True, exist_ok=True)
    output.chmod(0o700)
    options = XCUITestOptions().load_capabilities(settings["capabilities"])
    logging.info("Connect to the iPhone and open GoGoX for read-only inspection")
    driver = webdriver.Remote(settings["server_url"], options=options)
    try:
        driver.implicitly_wait(0)
        bundle_id = settings["capabilities"]["appium:bundleId"]
        WebDriverWait(driver, settings["wait_seconds"]).until(
            lambda session: session.query_app_state(bundle_id) == 4,
            message="GoGoX must be in the foreground before inspecting its screen.",
        )
        try:
            source = WebDriverWait(driver, settings["wait_seconds"]).until(
                interactive_screen,
                message="No visible controls appeared; GoGoX may still be loading.",
            )
        except TimeoutException:
            # Keep real failure evidence rather than silently treating splash as ready.
            driver.save_screenshot(str(output / "loading-timeout.png"))
            (output / "loading-timeout.png").chmod(0o600)
            raise
        tree = ElementTree.fromstring(source)
        if not any(node.get("type") == "XCUIElementTypeApplication" for node in tree.iter()):
            raise RuntimeError("The captured source is not a native iOS app hierarchy.")
        xml_path = output / "current-screen.xml"
        xml_path.write_text(source, encoding="utf-8")
        xml_path.chmod(0o600)
        png_path = output / "current-screen.png"
        png_path.write_bytes(driver.get_screenshot_as_png())
        png_path.chmod(0o600)
        logging.info("Saved private screenshot and UI hierarchy; no taps or data entry")
        return xml_path, png_path
    finally:
        driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    for path in capture_screen():
        print(Path(path).relative_to(ROOT))
