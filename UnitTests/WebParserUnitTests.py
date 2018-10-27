# Basic libraries
import unittest
# App Libraries
from WebParsing.web_parser import WebParser
from bs4 import BeautifulSoup

HTML_PAGE = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">This is the main story. In this story there are some emails.
First email is <a href="mailto:first@email.cz">here</a>. Another <a href="mailto:second@email.cz">email</a>
and the last email <a href="mailto:third@email.cz">link</a>.</p>

<strong class="first-class">There are a few classes to find. This is "first-class".</strong>
<i class="first-class">This is a "first-class" too</i>
<div class="second-class">and the last is "second-class"</div>
<div>All previous classes has different tags. This one has no class.</div>

Of course there are some inputs and buttons. To find elements by tag:
<br>

<button class="second-class">button 1</button>
<button>button 2</button>
<input type="text">input 1</input>
<input type="text">input 2</input>

<p>Of course there should be a table</p>
<table class="table-class">
<tr><td>first row, first col</td><td>first row, second col</td><td>first row, third col</td></tr>
<tr><td>second row, first col</td><td>second row, second col</td><td>second row, third col</td></tr>
</table>
"""

RESULT_PAGE_TEXT = """The Dormouse's story

The Dormouse's story
Once upon a time there were three little sisters; and their names were
Elsie,
Lacie and
Tillie;
and they lived at the bottom of a well.
This is the main story. In this story there are some emails.
First email is here. Another email
and the last email link.
There are a few classes to find. This is "first-class".
This is a "first-class" too
and the last is "second-class"
All previous classes has different tags. This one has no class.

Of course there are some inputs and buttons. To find elements by tag:

button 1
button 2
input 1
input 2

Of course there should be a table

first row, first colfirst row, second colfirst row, third col
second row, first colsecond row, second colsecond row, third col

"""


class WebParserTests(unittest.TestCase):
    """Tests for WebParser class"""

    def test__get_all_text__with_valid_page__should_return_text(self):
        parser = self._get_parser()

        result_text = parser.get_all_text()

        self.assertEqual(result_text, RESULT_PAGE_TEXT)

    def test__get_items_by_tag__with_valid_page__should_return_all_p_tags(self):
        parser = self._get_parser()

        result_tags = parser.get_items_by_tag("p")

        self.assertEqual(result_tags, ("The Dormouse's story", 'Once upon a time there were three little sisters; and their names were\nElsie,\nLacie and\nTillie;\nand they lived at the bottom of a well.', 'This is the main story. In this story there are some emails.\nFirst email is here. Another email\nand the last email link.', 'Of course there should be a table'))

    def test__get_items_by_tag__with_valid_page__should_return_all_div_tags(self):
        parser = self._get_parser()

        result_tags = parser.get_items_by_tag("div")

        self.assertEqual(result_tags, ('and the last is "second-class"', 'All previous classes has different tags. This one has no class.'))

    def test__get_items_by_tag__with_valid_page__should_return_all_button_tags(self):
        parser = self._get_parser()

        result_tags = parser.get_items_by_tag("button")

        self.assertEqual(result_tags,('button 1', 'button 2'))

    def test__get_items_by_tag__with_valid_page__should_return_all_td_tags(self):
        parser = self._get_parser()

        result_tags = parser.get_items_by_tag("td")

        self.assertEqual(result_tags, ('first row, first col', 'first row, second col', 'first row, third col', 'second row, first col', 'second row, second col', 'second row, third col'))

    def test__get_items_by_class__with_valid_page__should_return_first_class(self):
        parser = self._get_parser()

        result_classes = parser.get_items_by_class("first-class")

        self.assertEqual(result_classes, ('There are a few classes to find. This is "first-class".', 'This is a "first-class" too'))

    def test__get_items_by_class__with_valid_page__should_return_second_class(self):
        parser = self._get_parser()

        result_classes = parser.get_items_by_class("second-class")

        self.assertEqual(result_classes, ('and the last is "second-class"', 'button 1'))

    def test__get_all_links__with_valid_page__should_return_all_links(self):
        parser = self._get_parser()

        result_links = parser.get_all_links()

        self.assertEqual(result_links, ('http://example.com/elsie', 'http://example.com/lacie', 'http://example.com/tillie'))

    def test__get_all_emails__with_valid_page__should_return_all_links(self):
        parser = self._get_parser()

        result_emails = parser.get_all_emails()

        self.assertEqual(result_emails, ('first@email.cz', 'second@email.cz', 'third@email.cz'))

    @staticmethod
    def _get_parser():
        soup = BeautifulSoup(HTML_PAGE, WebParser.DEFAULT_PARSER)
        return WebParser(soup)
