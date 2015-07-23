# coding: utf-8

from __future__ import print_function
import re
import copy
import sass
import subprocess
import requests
import urlparse
from pyquery import PyQuery as pq
from BeautifulSoup import BeautifulSoup as bs
from lxml.html import HTMLParser, fromstring
import lxml.html as lh
UTF8_PARSER = HTMLParser(encoding='utf-8')


class Cloner:

    def __init__(self, url=None, selector=None, wrap=None):
        self.url = url
        self.selector = selector
        self.wrap = wrap
        self.s = requests.Session()
        self.d = None
        self.selected = None
        self.html = None
        self.css = None
        self.styles = []

    def _get(self, url):
        r = self.s.get(url)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            return r.text.encode('utf-8')

    def _remove_siblings(self, pq_ele):
        """
        Remove siblings and parent siblings
        """
        for ele in pq_ele.siblings():
            pq(ele).remove()
        parent = pq_ele.parent()
        if parent.length:
            self._remove_siblings(parent)

    def clean(self):
        """
        Get a clean document select by selector
        """
        html = self._get(self.url)
        self.d = pq(html)
        # Save style before romove
        for i in self.d('link[rel=stylesheet]'):
            i.make_links_absolute(self.url)
            self.styles.append(copy.deepcopy(i))
        self.selected = self.d(self.selector)
        self._remove_siblings(self.selected)
        for i in self.styles:
            self.d.prepend(i)
        return self.d

    def uncss(self, html):
        return subprocess.check_output(['uncss', '"{}"'.format(html)])

    def clean_css(self, css):
        css = re.sub(r'/\*[\s\S]+?\*/', '', css)
        css = re.sub(r'\n+', '\n', css)
        css = re.sub(r'.*@charset.*', '', css)
        css = re.sub(r'\*\w+', '', css)
        return css

    def scss_to_css(self, scss):
        return sass.compile(string=scss, output_style='expanded').encode('utf-8')

    def parse(self):
        html = self.clean()
        css = self.uncss(html)
        css = self.clean_css(css)
        if self.wrap:
            scss = '{}{{{}}}'.format(self.wrap, css)
            self.css = self.clean_css(self.scss_to_css(scss))
        else:
            self.css = css
        self.html = lh.tostring(self.selected[0], encoding='UTF-8', pretty_print=True, method="html")


if __name__ == '__main__':
    p = Cloner('http://www.shopex.cn/', '#happly', '.s-container')
    p.parse()
    print(p.html)
    print(p.css)
