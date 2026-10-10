"""Observed Review controls. Deliberately excludes the Place order control."""

from appium.webdriver.common.appiumby import AppiumBy

TITLE = (AppiumBy.ACCESSIBILITY_ID, "Review order")
CONTACT = (AppiumBy.ACCESSIBILITY_ID, "Order contact info")
CONTACT_EXPLANATION = (AppiumBy.ACCESSIBILITY_ID,
                       "Your driver will contact you to confirm order details")
FIELDS = (AppiumBy.CLASS_NAME, "XCUIElementTypeTextField")
SAVE_CONTACT = (AppiumBy.ACCESSIBILITY_ID, "Save")
TIP_20 = (AppiumBy.XPATH,
          '//XCUIElementTypeCell[XCUIElementTypeStaticText[@name="Add a tip"]]'
          '/XCUIElementTypeStaticText[@name="$20"]')


def summary_row(label):
    return (AppiumBy.XPATH,
            f'//XCUIElementTypeCell[XCUIElementTypeStaticText[@name="{label}"]]')
