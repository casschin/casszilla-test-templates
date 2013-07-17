#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from unittestzero import Assert
from requests.exceptions import Timeout


class Page(object):
    """Base class for all Pages"""

    def __init__(self, testsetup):
        """Constructor"""

        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self._selenium_root = hasattr(self, '_root_element') and self._root_element or self.selenium

    def open(self, url_fragment):
        """Open the specified url_fragment, which is relative to the base_url, in the current window."""
        self.selenium.get(self.base_url + url_fragment)
        self.is_the_current_page

    def select_option(self, value, locator):
        self.is_element_present(locator)
        dropdown = self.find_element(locator)
        all_options = dropdown.find_elements_by_tag_name("option")
        option_found = False
        for option in all_options:
            if option.get_attribute("value") == value:
                option_found = True
                option.click()
                break
        if option_found is False:
            raise Exception("Could not select option '%s' because it was not found." % value)

    def resize_window(self, width, height):
        """Resizes the window."""
        self.selenium.set_window_size(width, height)

    def click_element(self, locator):
        try:
            self.find_element(locator).click()
            return True
        except NoSuchElementException:
            return False

    def input_text(self, text, locator):
        try:
            self.clear_input(locator)
            self.find_element(locator).send_keys(text)
            return True
        except NoSuchElementException:
            return False

    def clear_input(self, locator):
        try:
            self.find_element(locator).clear()
            return True
        except NoSuchElementException:
            return False

    @property
    def page_title(self):
        """
            Return the page title from Selenium.
            This is different from _page_title,
            which is defined for a specific page object and is the expected title of the page.
        """
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def is_the_current_page(self):
        """Return true if the actual page title matches the expected title stored in _page_title."""
        if self._page_title:
            Assert.equal(self.page_title, self._page_title,
                         "Expected page title: %s. Actual page title: %s" % (self._page_title, self.page_title))
        return True

    def is_element_present(self, locator):
        """
        Return true if the element at the specified locator is present in the DOM.
        Note: It returns false immediately if the element is not found.
        """
        self.selenium.implicitly_wait(0)
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set the implicit wait back
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, locator):
        """
        Return true if the element at the specified locator is visible in the browser.
        Note: It uses an implicit wait if it cannot find the element immediately.
        """
        try:
            return self.find_element(locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def is_element_not_visible(self, locator):
        """
        Return true if the element at the specified locator is not visible in the browser.
        Note: It returns true immediately if the element is not found.
        """
        self.selenium.implicitly_wait(0)
        try:
            return not self.selenum.find_element(locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return True
        finally:
            # set the implicit wait back
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_text_visible(self, text, locator):
        """Return true if the text at the specified locator is visible in the browser."""
        self.is_element_present(locator)
        page_text = self.find_element(locator).text
        Assert.equal(page_text, text, "Cannot find text '%s' on the page." % text)
        return True

    def is_text_not_visible(self, text, locator):
        """Return true the text at the specified locator is not visible in the browser."""
        self.is_element_present(locator)
        page_text = self.find_element(locator).text
        Assert.not_equal(page_text, text, "Found text '%s' on the page." % text)
        return True

    def are_link_destinations_correct(self, link_list):
        """Return true if the expected links exist on a page."""
        bad_links = []
        for link in link_list:
            if link.get('url_suffix') is not None:
                url = self.link_destination(link.get('locator'))
                if not url.endswith(link.get('url_suffix')):
                    bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))
        return True

    def wait_for_element_present(self, locator):
        """Wait for the element at the specified locator to be present in the DOM."""
        count = 0
        while not self.is_element_present(locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(str(locator) + ' has not loaded')

    def wait_for_element_visible(self, locator):
        """Wait for the element at the specified locator to be visible in the browser."""
        count = 0
        while not self.is_element_visible(locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(str(locator) + " is not visible")

    def wait_for_element_not_present(self, locator):
        """Wait for the element at the specified locator to be not present in the DOM."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(lambda s: len(self.find_elements(locator)) < 1)
            return True
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def get_url_current_page(self):
        """Return the url for the current page."""
        return(self.selenium.current_url)

    def find_element(self, locator):
        """Return the element at the specified locator."""
        return self._selenium_root.find_element(*locator)

    def find_elements(self, locator):
        """Return a list of elements at the specified locator."""
        return self._selenium_root.find_elements(*locator)

    def link_destination(self, locator):
        """Return the href attribute of the element at the specified locator."""
        link = self.find_element(locator)
        return link.get_attribute('href')

    def image_source(self, locator):
        """Return the src attribute of the element at the specified locator."""
        link = self.find_element(locator)
        return link.get_attribute('src')


class PageRegion(Page):
    """Base class for a page region (generally an element in a list of elements)."""

    def __init__(self, testsetup, element):
        self._root_element = element
        Page.__init__(self, testsetup)
