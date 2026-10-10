"""Native sheet controls observed in the installed English app."""

from appium.webdriver.common.appiumby import AppiumBy

PICKUP_TITLE = (AppiumBy.ACCESSIBILITY_ID, "Pick-up time")
WHEELS = (AppiumBy.CLASS_NAME, "XCUIElementTypePickerWheel")
OK = (AppiumBy.ACCESSIBILITY_ID, "OK")
