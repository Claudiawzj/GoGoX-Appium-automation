"""Signup controls captured on the installed app on 11 October 2026.

GoGoX reuses its login identifiers on signup. The signup title guards their use.
"""

from appium.webdriver.common.appiumby import AppiumBy

TITLE = (AppiumBy.ACCESSIBILITY_ID, "Sign up for a Hong Kong account")
PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "login_password__input__password")
SIGN_UP = (AppiumBy.ACCESSIBILITY_ID, "login_password__button__login")
