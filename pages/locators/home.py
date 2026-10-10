"""Observed in GoGoX 7.111.0, Hong Kong, English UI on 10 October 2026.

The XML names were read from the app. The home-control test checks uniqueness and
visibility through Appium. FROM/TO are empty-route placeholders; populated route
controls need separate inspection before implementing route edits.
"""

from appium.webdriver.common.appiumby import AppiumBy

MENU = (AppiumBy.ACCESSIBILITY_ID, "home__header__navigation_icon__menu")
TRANSPORT = (AppiumBy.ACCESSIBILITY_ID, "Transport")
FROM = (AppiumBy.ACCESSIBILITY_ID, "Where from?")
TO = (AppiumBy.ACCESSIBILITY_ID, "Where to?")
NEXT = (AppiumBy.ACCESSIBILITY_ID, "Next")
