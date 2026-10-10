"""Select exact search results and wait for the automatic return to home."""

import logging

from pages.base_page import BasePage
from pages.locators import home, location


class LocationPage(BasePage):
    def _choose(self, query, result, home_field, description):
        logging.info("STEP: Search for the configured %s and select its exact result", description)
        # Done marks this editor, but is not a confirmation action after selection.
        # Selecting a result returns automatically; an early Done tap interrupted
        # destination persistence during inspection.
        self.visible_control(location.DONE)
        field = self.visible_control(location.SEARCH)
        field.clear()
        field.send_keys(query)
        self.wait.until(lambda session: self.visible_control(location.SEARCH)
                        .get_attribute("value") == query,
                        message="Location query did not match the configured text.")
        self.visible_control(location.exact_result(result)).click()
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
