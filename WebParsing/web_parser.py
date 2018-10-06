# Basic libraries
import re
from urllib.parse import urljoin
# Third-party libraries
import requests
from bs4 import BeautifulSoup


DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 'AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/61.0.3163.100 ' 'Safari/537.36' }


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

    def get_all_links(self):
        links = [l for l in self._get_all_links() if not l.startswith("mailto:")]
        return tuple(links)

    def get_all_emails(self):
        links = [l for l in self._get_all_links() if l.startswith("mailto:")]
        return tuple(links)

    def get_all_following_links(self, level):
        following_links = [self._get_all_links()]

        for l in range(level):
            pass

        return following_links

    # -----------------
    # Private methods
    # -----------------

    def _get_all_links(self):
        return [l["href"] for l in self._soup.find_all('a', href=True) if not l["href"].startswith("#")]

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
