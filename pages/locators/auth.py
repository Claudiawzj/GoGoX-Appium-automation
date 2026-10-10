"""Observed English email/password controls in GoGoX 7.111.0 on 10 October 2026."""

from appium.webdriver.common.appiumby import AppiumBy

EMAIL = (AppiumBy.ACCESSIBILITY_ID, "login_email_number__input__email_number")
EMAIL_NEXT = (AppiumBy.ACCESSIBILITY_ID, "login_email_number__button__next")
PASSWORD_TITLE = (AppiumBy.ACCESSIBILITY_ID, "Log in to your personal account")
PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "login_password__input__password")
LOG_IN = (AppiumBy.ACCESSIBILITY_ID, "login_password__button__login")
BACK = (AppiumBy.ACCESSIBILITY_ID, "back")
CLOSE = (AppiumBy.ACCESSIBILITY_ID, "close")
