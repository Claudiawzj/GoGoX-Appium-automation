"""Observed in GoGoX 7.111.0, Hong Kong, English UI on 10 October 2026.

The XML names were read from the app. The home-control test checks uniqueness and
visibility through Appium. FROM/TO are empty-route placeholders. FROM_FIELD and
TO_FIELD use the observed table cells for empty and populated route editing.
"""

from appium.webdriver.common.appiumby import AppiumBy

MENU = (AppiumBy.ACCESSIBILITY_ID, "home__header__navigation_icon__menu")
TRANSPORT = (AppiumBy.ACCESSIBILITY_ID, "Transport")
FROM = (AppiumBy.ACCESSIBILITY_ID, "Where from?")
TO = (AppiumBy.ACCESSIBILITY_ID, "Where to?")
NEXT = (AppiumBy.ACCESSIBILITY_ID, "Next")
# Observed table structure: first Cell is pickup, second Cell is destination.
# Unlike placeholder labels, these controls work with empty and populated routes.
FROM_FIELD = (AppiumBy.IOS_CLASS_CHAIN,
              "**/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeTextView")
TO_FIELD = (AppiumBy.IOS_CLASS_CHAIN,
            "**/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeTextView")
