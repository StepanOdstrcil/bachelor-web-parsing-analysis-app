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

URL_REGEX = (r'^(?:http|ftp)s?://'  # http:// or https://
             r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
             r'localhost|'  # localhost...
             r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
             r'(?::\d+)?'  # optional port
             r'(?:/?|[/?]\S+)$')

DEFAULT_PARSER = "html.parser"


class WebParser:
    """Class used for parsing web and its statistics"""

    def __init__(self):
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
                self._soup = self._get_soup_from_url(url)
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
        """
        Gets all links from page
        :return: all links as list
        """
        links = [l for l in self._get_all_links(self._soup) if not l.startswith("mailto:")]
        return tuple(links)

    def get_all_emails(self):
        """
        Gets all emails from page (href has mailto: before email)
        :return: all emails from page as list
        """
        links = [l for l in self._get_all_links(self._soup) if l.startswith("mailto:")]
        return tuple(links)

    def get_all_following_links(self, level):
        """
        Gets all links defined by level. It gets all links in page. Then second level is all links from links at
        first level. Next level (third) is all links from all links at second level. Etc...
        :param level: how deep should getting links go
        :return: list of lists of all links. Each list is level deeper. First is base page, second is all links from
        links at first level.
        """
        following_links = [self._get_all_links(self._soup)]

        for l in range(0, level - 1):
            links = following_links[l]
            found_links = []
            for link in links:
                if self._is_url_valid(link) and self._is_url_html(link):
                    found_links.extend(self._get_all_links_from_url(link))

            following_links.append(found_links)

        return following_links

    # -----------------
    # Private methods
    # -----------------

    @staticmethod
    def _is_url_valid(url):
        regex = re.compile(URL_REGEX, re.IGNORECASE)
        return re.match(regex, url) is not None

    @staticmethod
    def _is_url_html(url):
        try:
            r = requests.head(url)
        except requests.exceptions.ConnectionError as ex:
            # TODO: LOG
            print(f"Error: message: {ex}, url: {url}")
            return False

        return "text/html" in r.headers["content-type"] if "content-type" in r.headers else False

    @staticmethod
    def _get_all_links(soup):
        """
        Get all links contained in soup class
        :param soup: BeautifulSoup class containing loaded page
        :return: all links as list
        """
        return [l["href"] for l in soup.find_all('a', href=True) if not l["href"].startswith("#")]

    @staticmethod
    def _get_all_links_from_url(url):
        """
        Gets all links in defined URL (request will happen)
        :param url: to get links from
        :return: all links from URL in list
        """
        soup = WebParser._get_soup_from_url(url)
        return WebParser._get_all_links(soup)

    @staticmethod
    def _get_soup_from_url(url):
        """
        Initializes BeautifulSoup from defined URL
        :param url: to get soup from
        :return: BeautifulSoup class with page from URL
        """
        page = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        return BeautifulSoup(page.text, DEFAULT_PARSER)
