"""Time/vehicle controls and selection indicators observed on 10 October 2026."""

from appium.webdriver.common.appiumby import AppiumBy

TITLE = (AppiumBy.ACCESSIBILITY_ID, "Time and vehicle")
HOURLY_RENTAL = (AppiumBy.ACCESSIBILITY_ID, "Hourly rental")
VAN = (AppiumBy.ACCESSIBILITY_ID, "Van")
VAN_CARD = (AppiumBy.XPATH,
            '//XCUIElementTypeCell[XCUIElementTypeStaticText[@name="Van"]]')
BACK = (AppiumBy.ACCESSIBILITY_ID, "back")
CALENDAR = (AppiumBy.ACCESSIBILITY_ID, "calendar")
PICKUP_SUMMARY = (AppiumBy.XPATH,
                  '//XCUIElementTypeImage[@name="calendar"]/following-sibling::XCUIElementTypeStaticText')
FOUR_HOURS = (AppiumBy.ACCESSIBILITY_ID, "4 hours")
VAN_SELECTED = (AppiumBy.XPATH,
                '//XCUIElementTypeCell[XCUIElementTypeStaticText[@name="Van"]]'
                '//XCUIElementTypeImage[@name="card-check"]')
# This shared footer has a misleading internal ID. Only use it while this page's
# Time and vehicle title and required selections are verified; it displays Next.
NEXT = (AppiumBy.ACCESSIBILITY_ID, "ggv__order_detail__footer__button__review_order")
