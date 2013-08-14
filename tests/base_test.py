#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def get_response_code(self, url, timeout):
        """Return the response code for a get request to the specified url."""
        # this sets max_retries to 5
        requests.adapters.DEFAULT_RETRIES = 5
        try:
            r = requests.get(url, verify=False, allow_redirects=True, timeout=timeout, headers={'User-Agent': 'a user agent'})
            return r.status_code
        except requests.Timeout:
            return 408

    def make_absolute(self, url, base_url):
        """Return the url argument as an absolute url."""
        if url.startswith('http'):
            return url
        return base_url + url

    def are_links_are_valid(self, mozwebqa, link_list):
        bad_links = []
        for link in link_list:
            if link['href'] != '#':
                url = self.make_absolute(link['href'], mozwebqa.base_url)
                response_code = self.get_response_code(url, mozwebqa.timeout)
                if response_code != requests.codes.ok:
                    bad_links.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_links), '%s bad urls found: ' % len(bad_links) + ', '.join(bad_links))

    def are_links_are_visible(self, browser_width, page, link_list):
        bad_links = []
        for link in link_list:
            if link.get('min-width') > browser_width or link.get('min-width') == None:
                if not page.is_element_visible(*link.get('locator')):
                    bad_links.append('The link at %s is not visible' % link.get('locator')[1:])
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))
