"""Observed native location search controls in GoGoX 7.111.0 on 10 October 2026."""

from appium.webdriver.common.appiumby import AppiumBy

SEARCH = (AppiumBy.CLASS_NAME, "XCUIElementTypeTextView")
DONE = (AppiumBy.ACCESSIBILITY_ID, "Done")
CLOSE = (AppiumBy.ACCESSIBILITY_ID, "close")


def exact_result(address):
    return (AppiumBy.ACCESSIBILITY_ID, address)
