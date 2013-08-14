#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from time import sleep

from bs4 import BeautifulSoup  # Only required for the test that doesn't use Selenium
import pytest
import requests
from unittestzero import Assert

from pages.home import HomePage
from base_test import BaseTest


class TestHomePage(BaseTest):

    @pytest.mark.nondestructive
    def test_that_hoverover_image_displays(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        home_page.hover_element(home_page._hover_link_locator)
        Assert.equal(home_page.is_element_visible(home_page._hover_image_locator), True)

    @pytest.mark.nondestructive
    def test_that_page_has_list_items(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        expected_item_count = 4
        Assert.equal(home_page.list_items_count, expected_item_count,
            'Expected %s items, but found %s.' % (expected_item_count, home_page.list_items_count))

    @pytest.mark.nondestructive
    def test_that_list_excerpts_are_visible(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        list_items = home_page.list_items
        for list_item in list_items:
            Assert.equal(list_item.link_present, True,
                "Element at '%s' was not found." % list_item._item_link_locator[1])

    @pytest.mark.nondestructive
    def test_click_element(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        home_page.click_element(home_page._click_link_locator)
        home_page.is_text_visible('Yes.', home_page._click_label_locator)

    @pytest.mark.nondestructive
    def test_input_text(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        home_page.input_text('Just some text.', home_page._input_field_locator)
        home_page.click_element(home_page._submit_button_locator)
        home_page.is_text_visible('Just some text.', home_page._input_value_locator)

    @pytest.mark.nondestructive
    def test_window_resizing(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.resize_window(500, 900)
        home_page.go_to_page()
        home_page.resize_window(600, 900)
        home_page.resize_window(700, 900)
        home_page.resize_window(800, 900)
        home_page.resize_window(900, 900)
        home_page.resize_window(1000, 900)
        home_page.resize_window(1100, 900)
        home_page.resize_window(1200, 900)
        home_page.resize_window(1300, 900)
        home_page.resize_window(1400, 900)

    @pytest.mark.nondestructive
    def test_that_text_is_visible(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        text = "Casszilla!"
        home_page.is_text_visible(text, home_page._page_header)

    @pytest.mark.nondestructive
    def test_that_text_is_not_visible(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        text = "Mozilla!"
        home_page.is_text_not_visible(text, home_page._page_header)

    @pytest.mark.nondestructive
    def test_that_drop_down_selector_changes_value(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        selected_value = "dropdown option 4"
        home_page.select_option(selected_value, home_page._drop_down_locator)
        home_page.is_text_visible(selected_value, home_page._drop_down_selected_value_locator)

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_specific_links_are_valid(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        url = mozwebqa.base_url + home_page._page_url_suffix
        page_response = requests.get(url)
        html = BeautifulSoup(page_response.content)
        # For the test page, we grab a specfic section of links
        # To test all links on a page replace with links = html.findAll('a')
        links = html.find(id="valid-links").find_all('a')
        bad_links = []
        for link in links:
            url = self.make_absolute(link['href'], mozwebqa.base_url)
            response_code = self.get_response_code(url, mozwebqa.timeout)
            if response_code != requests.codes.ok:
                bad_links.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_links), '%s bad urls found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_all_links_are_valid(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        url = mozwebqa.base_url + home_page._page_url_suffix
        page_response = requests.get(url)
        html = BeautifulSoup(page_response.content)
        links = html.findAll('a')
        bad_links = []
        for link in links:
            url = self.make_absolute(link['href'], mozwebqa.base_url)
            response_code = self.get_response_code(url, mozwebqa.timeout)
            if response_code != requests.codes.ok:
                bad_links.append('%s is a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_links), '%s bad urls found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_that_link_destinations_are_correct(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        home_page.are_link_destinations_correct(home_page.valid_link_list)
