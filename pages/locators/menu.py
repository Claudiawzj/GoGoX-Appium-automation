"""Guest and personal-account menu controls observed on 10 October 2026."""

from appium.webdriver.common.appiumby import AppiumBy

LOG_IN_OR_SIGN_UP = (AppiumBy.ACCESSIBILITY_ID, "sidebar__link__log_in_or_sign_up")
GUEST = (AppiumBy.ACCESSIBILITY_ID, "Hi guest")
YOUR_ORDERS = (AppiumBy.ACCESSIBILITY_ID, "Your orders")
PERSONAL_ACCOUNT = (AppiumBy.ACCESSIBILITY_ID, "account personal")
PERSONAL = (AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeButton" AND name == "Personal"')
