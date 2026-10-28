# from bs4.replacer import SoupReplacer
from bs4 import BeautifulSoup, SoupReplacer


html = "<p>Hello <b>world</b></p>"
html_nested ="<div><b>OUTER <blockquote>INNER</blockquote> END</b><p>Next</p></div>"
html_single = "<div><b>Hello"

class TestSoupReplacer:
    def test_replaces_tags_works(self):
        replacer = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(html, "html.parser",replacer=replacer)
        print(soup.prettify())
        blockquote = soup.find("blockquote")

        assert blockquote is not None
        assert blockquote.get_text() == "world"
        assert soup.find("b") is None


    def test_nested_tags_replace_works_w_structure(self):
        replacer = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(html_nested, "html.parser",replacer=replacer)
        print(soup.prettify())
        blockquote = soup.find_all("blockquote")

        assert len(blockquote) == 2
        assert soup.find("b") is None
        assert blockquote[1].find_parent("blockquote") is blockquote[0]
        p = soup.find("p")
        assert p is not None
        assert p.parent is soup.find("div")




