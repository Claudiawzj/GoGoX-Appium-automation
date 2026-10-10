"""Select exact search results and wait for the automatic return to home."""

import logging

from pages.base_page import BasePage
from pages.locators import home, location


class LocationPage(BasePage):
    def _choose(self, query, result, home_field, description):
        logging.info("STEP: Search for the configured %s and select its exact result", description)
        # The editor may return automatically or keep the resolved address for Done.
        # Wait for the selected address before confirming a remaining editor.
        self.visible_control(location.DONE)
        field = self.visible_control(location.SEARCH)
        field.clear()
        field.send_keys(query)
        self.wait.until(lambda session: self.visible_control(location.SEARCH)
                        .get_attribute("value") == query,
                        message="Location query did not match the configured text.")
        self.visible_control(location.exact_result(result)).click()

        def selection_settled(session):
            if any(item.is_displayed() for item in session.find_elements(*home.MENU)):
                return "home"
            fields = [item for item in session.find_elements(*location.SEARCH)
                      if item.is_displayed()]
            results = [item for item in session.find_elements(*location.exact_result(result))
                       if item.is_displayed()]
            if len(fields) == 1 and fields[0].get_attribute("value") == result and not results:
                return "editor"
            return False

        state = self.wait.until(selection_settled,
                                message="Selected address did not finish resolving.")
        if state == "editor":
            self.visible_control(location.DONE).click()
        self.visible_control(home.MENU)

        def saved_address(session):
            matches = [item for item in session.find_elements(*home_field)
                       if item.is_displayed()]
            return len(matches) == 1 and matches[0].get_attribute("value") == result

        self.wait.until(saved_address,
                        message="Selected location did not persist in its home route field.")
        return self

    def choose_pickup(self, query, result):
        return self._choose(query, result, home.FROM_FIELD, "pickup")

    def choose_destination(self, query, result):
        return self._choose(query, result, home.TO_FIELD, "destination")
