"""Contact editing, tip and read-only review assertions. No submission method."""

import logging

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from pages.locators import review
from utils.pickup_plan import normalize_label


class ReviewPage(BasePage):
    def wait_for_screen(self):
        self.visible_control(review.TITLE)
        return self

    def verify_route_and_pickup(self, route, plan):
        self.wait_for_screen()
        for value in (route["from_result"], route["to_result"], "Van"):
            self.visible_control((AppiumBy.ACCESSIBILITY_ID, value))
        self.wait.until(lambda session: any(
            normalize_label(e.get_attribute("label")) == plan.summary_label
            for e in session.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
            if e.is_displayed()), message="Review pickup differs from the configured plan.")

    def _contact_fields(self):
        fields = sorted([e for e in self.driver.find_elements(*review.FIELDS)
                         if e.is_displayed()], key=lambda e: e.rect["y"])
        if len(fields) != 3:
            raise ValueError("Contact sheet must expose name, phone and extension fields.")
        return fields

    def save_dummy_contact(self, contact):
        self.wait_for_screen()
        logging.info("STEP: Open Order contact info and save configured dummy details")
        self.visible_control(review.CONTACT).click()
        self.visible_control(review.CONTACT_EXPLANATION)
        for index, key in enumerate(("name", "phone", "extension")):
            # Reacquire fields after each edit: the sheet relayouts as focus changes.
            value = contact[key]
            if self._contact_fields()[index].get_attribute("value") != value:
                field = self._contact_fields()[index]
                field.click()
                field.clear()
                if value:
                    try:
                        field.send_keys(value)
                    except Exception:
                        raise RuntimeError("Could not enter configured dummy contact data.") from None
            self.wait.until(lambda session: (self._contact_fields()[index]
                            .get_attribute("value") or "") == value,
                            message="Contact field did not retain the configured value.")
        # Verify all fields together immediately before Save.
        assert [(e.get_attribute("value") or "") for e in self._contact_fields()] == [
            contact[key] for key in ("name", "phone", "extension")]
        self.visible_control(review.SAVE_CONTACT).click()
        self.wait.until(lambda session: not any(e.is_displayed() for e in
                        session.find_elements(*review.CONTACT_EXPLANATION)),
                        message="Contact sheet did not close after Save.")
        self.visible_control((AppiumBy.ACCESSIBILITY_ID,
                              f'{contact["name"]}・{contact["phone"]}'))
        return self.wait_for_screen()

    def _scroll_to(self, locator):
        for _ in range(5):
            matches = [e for e in self.driver.find_elements(*locator) if e.is_displayed()]
            if len(matches) == 1:
                return matches[0]
            before = self.driver.page_source
            self.driver.execute_script("mobile: swipe", {"direction": "up"})
            self.wait.until(lambda session: session.page_source != before,
                            message="Review did not change after scrolling.")
        return self.visible_control(locator)

    def add_twenty_dollar_tip(self):
        self.wait_for_screen()
        logging.info("STEP: Select HK$20 inside Add a tip; never tap the footer")
        self._scroll_to(review.TIP_20).click()
        return self

    def assert_required_summary(self):
        logging.info("STEP: Verify required services in the review fee breakdown")
        expected = {
            "Base fee (4 hr rental)": None,
            "Driver tip": "$20",
            "Passengers (3)": "$0", "Borrow a trolley": "$10",
            "Goods longer than 6 ft": "$20", "Pet-friendly driver": "$10",
            "Premium Van": "$20", "English-speaking driver": "$5",
            "Cross-Harbour Tunnel (Hung Hom)": "$50",
            "Cargo compensation - Basic": "$10", "Move door-to-door ": "Quote",
        }
        for label, amount in expected.items():
            row = self._scroll_to(review.summary_row(label))
            if amount:
                assert any(e.get_attribute("name") == amount for e in
                           row.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")), \
                    "Required review fee differs from the inspected selection."
        return self
