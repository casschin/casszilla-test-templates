#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.page import Page


class Base(Page):
    """
    Base class for global project specific functions
    """

    @property
    def footer(self):
        """Return the common Footer region."""
        return self.Footer(self.testsetup)

    class Footer(Page):
        """The common Footer region that is present on every page."""

        # The locators in this list contain examples of positional locators, a unique css locator,
        # and a link text locator
        copyright_links_list = [
            {
                'locator': (By.CSS_SELECTOR, 'footer > a:nth-of-type(1)'),
                'url_suffix': 'http://about.me/cass',
            }, {
                'locator': (By.CSS_SELECTOR, 'footer > a:nth-of-type(2)'),
                'url_suffix': 'http://twitter.com/casschin'
            },
        ]
