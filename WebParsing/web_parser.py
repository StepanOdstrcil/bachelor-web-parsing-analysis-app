# Basic libraries
import re
# Third-party libraries
import requests
from bs4 import BeautifulSoup


class WebParser:
    """Class used for parsing web and its statistics"""

    def __init__(self):
        self._page = None
        self._soup = None

    # -----------------
    # Properties
    # -----------------

    # -----------------
    # Public methods
    # -----------------

    def load_page(self, url):
        """
        Loads page from defined URL
        :param url: url to get page from
        :return: None
        """
        if self._is_url_valid(url):
            if self._is_url_html(url):
                self._page = requests.get(url)
                self._soup = BeautifulSoup(self._page.text, "html.parser")
            else:
                raise Exception("Page from URL is not HTML")
        else:
            raise Exception("URL is not valid")

    def get_all_text(self):
        """
        Gets all text in loaded page
        :return: text as string
        """
        return self._soup.get_text()

    def get_items_by_tag(self, tag):
        """
        Gets all text by tag
        :param tag: name of the tag. Can be multiple, for example: 'td a' like table cell with 'a' tag in it
        :return: all text in all tags as tuple
        """
        items = [t.get_text() for t in self._soup.select(tag)]
        return tuple(items)

    def get_items_by_class(self, cls):
        """
        Gets all text inside all tags with class in parameter
        :param cls: name of the class
        :return: all text in elements defined by class in parameter as tuple
        """
        items = [t.get_text() for t in self._soup.find_all("html_element", class_=cls)]
        return tuple(items)

    # -----------------
    # Private methods
    # -----------------

    @staticmethod
    def _is_url_valid(url):
        regex = re.compile(r'^(?:http|ftp)s?://'  # http:// or https://
                           r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                           r'localhost|'  # localhost...
                           r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                           r'(?::\d+)?'  # optional port
                           r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    @staticmethod
    def _is_url_html(url):
        r = requests.head(url)
        return "text/html" in r.headers["content-type"]
