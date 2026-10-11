"""Settings/profile controls captured on the installed app on 10 October 2026."""

from appium.webdriver.common.appiumby import AppiumBy

SETTINGS = (AppiumBy.ACCESSIBILITY_ID, "Settings")
PERSONAL = (AppiumBy.ACCESSIBILITY_ID, "Personal")
PROFILE = (AppiumBy.ACCESSIBILITY_ID, "Profile")
LOG_OUT = (AppiumBy.ACCESSIBILITY_ID,
           "profile__list__button__log_out_of_your_personal_account")
CLOSE = (AppiumBy.ACCESSIBILITY_ID, "close")
