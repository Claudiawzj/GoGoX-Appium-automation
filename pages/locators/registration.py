"""Screenshot-derived signup controls; native identifiers remain unverified.

The app exposes login inputs/buttons as Other elements with semantic identifiers.
Match the password/signup role, or their visible labels, without assuming an exact
new identifier. Page actions require a unique visible match and the signup title.
"""

from appium.webdriver.common.appiumby import AppiumBy

TITLE = (AppiumBy.ACCESSIBILITY_ID, "Sign up for a Hong Kong account")
PASSWORD = (AppiumBy.IOS_PREDICATE,
            'type == "XCUIElementTypeSecureTextField" OR '
            '((type == "XCUIElementTypeOther" OR type == "XCUIElementTypeTextField") '
            'AND (name CONTAINS[c] "__input__password" '
            'OR name == "Password" OR label == "Password"))')
SIGN_UP = (AppiumBy.IOS_PREDICATE,
           '(type == "XCUIElementTypeOther" OR type == "XCUIElementTypeButton" '
           'OR type == "XCUIElementTypeStaticText") '
           'AND (name ENDSWITH[c] "__button__sign_up" '
           'OR name ENDSWITH[c] "__button__signup" '
           'OR name == "Sign up" OR label == "Sign up")')
