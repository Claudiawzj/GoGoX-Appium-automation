"""Initial Order details markers observed on 10 October 2026; extras actions pending."""

from appium.webdriver.common.appiumby import AppiumBy

TITLE = (AppiumBy.ACCESSIBILITY_ID, "Order details")
COMPENSATION = (AppiumBy.ACCESSIBILITY_ID, "Cargo compensation")
BASIC = (AppiumBy.ACCESSIBILITY_ID, "Basic")
BACK = (AppiumBy.ACCESSIBILITY_ID, "back")

TUNNEL_EXPLANATION = (AppiumBy.ACCESSIBILITY_ID, "Your driver will charge the full toll fee.")
TUNNEL_CONFIRM = (AppiumBy.ACCESSIBILITY_ID, "Confirm")
TUNNEL_CHOICE = (AppiumBy.ACCESSIBILITY_ID, "Cross-Harbour Tunnel (Hung Hom)")
REVIEW = (AppiumBy.ACCESSIBILITY_ID, "ggv__order_detail__footer__button__review_order")


def row(label):
    return (AppiumBy.XPATH,
            f'//XCUIElementTypeCell[XCUIElementTypeStaticText[@name="{label}"]]')


def count(label, value):
    return (AppiumBy.XPATH,
            f'{row(label)[1]}/XCUIElementTypeStaticText[@name="{value}"]')
