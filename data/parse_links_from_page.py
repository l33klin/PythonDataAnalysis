#!/usr/bin/env python
# encoding: utf-8

__author__ = 'klin'


import os
import sys
import re
from HTMLParser import HTMLParser

sys.path.append('..')
import log

path = os.path.join('.', 'raw_page', '1.USA.gov Archives_ 2 June - 31 December 2011.html')
link_pattern = '.*1usagov.measuredvoice.com/bitly_archive/usagov_bitly_data.*\.gz'
links_file = os.path.join('.', 'file_links')

class ParsePatternLinks(HTMLParser):
    """

    """

    def __init__(self, pattern=''):
        HTMLParser.__init__(self)
        self.link_comp = re.compile(pattern)
        self.target_links = list()
        pass

    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        if self.link_comp.match(value):
                            self.target_links.append(value)
                        else:
                            print 'Match fail:', self.link_comp.match(value)

    def get_target_links(self):
        return self.target_links


if __name__ == '__main__':

    page_content = ''

    with open(path) as f:
        page_content = f.read()

    iParser = ParsePatternLinks(pattern=link_pattern)
    iParser.feed(page_content)
    links = iParser.get_target_links()

    with open(links_file, 'w') as f:
        for link in links:
            f.write(link + '\n')
            f.flush()

    pass
