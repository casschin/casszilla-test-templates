#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import datetime

from selenium.webdriver.common.by import By

from base import Base
from page import PageRegion


class HomePage(Base):
    """This Page Object models the Casszilla test page (http://cassch.in/casszilla/)."""

    _page_url_suffix = ''
    # The title of this page, which is used by is_the_current_page() in page.py
    _page_title = u'Casszilla!'

    # Locators for the home page
    _page_header = (By.ID, 'page-header')

    # Drop down locators
    _drop_down_locator = (By.ID, 'dropdown')
    _drop_down_selected_value_locator = (By.ID, 'dropdown-selected-value')

    # Hover locators
    _hover_div_locator = (By.ID, 'hover-elements')
    _hover_link_locator = (By.ID, 'hover-link')
    _hover_image_locator = (By.ID, 'hover-image')

    # Link locators, which can be used for checking visibility, accuracy and validity of links
    _valid_link_locator = (By.ID, 'valid-link')
    _valid_link_one_locator = (By.CSS_SELECTOR, '#valid-links > li:nth-of-type(1) > a')
    _valid_link_two_locator = (By.CSS_SELECTOR, '#valid-links > li:nth-of-type(2) > a')
    _valid_link_three_locator = (By.CSS_SELECTOR, '#valid-links > li:nth-of-type(3) > a')
    valid_link_list = [
        {
            'locator': (By.CSS_SELECTOR, '#valid-links > li:nth-of-type(1) > a'),
            'url_suffix': 'http://google.com/',
        }, {
            'locator': (By.CSS_SELECTOR, '#valid-links > li:nth-of-type(2) > a'),
            'url_suffix': 'http://yahoo.com/',
        }, {
            'locator': (By.CSS_SELECTOR, '#valid-links > li:nth-of-type(3) > a'),
            'url_suffix': 'http://bing.com/',
        },
    ]

    # Click element locators
    _click_link_locator = (By.ID, 'click')
    _click_label_locator = (By.ID, 'clicked')

    # Input field locators
    _input_field_locator = (By.ID, 'input-field')
    _submit_button_locator = (By.ID, 'submit-button')
    _input_value_locator = (By.ID, 'input-value')

    # Item list locators
    _list_items_locator = (By.CSS_SELECTOR, '#item-list > li.item')


    def go_to_page(self, url_suffix = _page_url_suffix):
        """Open the home page."""
        self.open(url_suffix)

    @property
    def list_items_count(self):
        """Return the number of list items on the home page."""
        return len(self.find_elements(self._list_items_locator))

    @property
    def list_items(self):
        """Return a list of new items, each of which is a single list item from the home page."""
        return [self.ListItem(self.testsetup, web_element)
                for web_element in self.find_elements(self._list_items_locator)]

    class ListItem(PageRegion):
        """Allows each list item on the home page to be treated as a separate object."""

        _item_title_locator = (By.CSS_SELECTOR, '.item-title')
        _item_excerpt_locator = (By.CSS_SELECTOR, '.excerpt')
        _item_link_locator = (By.CSS_SELECTOR, '.item-link')

        @property
        def title(self):
            """Return the title of the list item."""
            return self.find_element(self._item_title_locator).text

        @property
        def excerpt_present(self):
            """Return True if the item is a post (as opposed to an event)."""
            return self.is_element_present(self._item_excerpt_locator)

        @property
        def link_present(self):
            """Return trues if the item link is present"""
            return self.is_element_present(self._item_link_locator)

