from bs4 import BeautifulSoup, SoupReplacer

html = "<p>Hello <b>world</b></p>"
html_nested ="<div><b>OUTER <blockquote>INNER</blockquote> END</b><p>Next</p></div>"
html_single = "<div><b>Hello"

class TestSoupXformer:
    def test_name_xformer_works(self):
        replacer = SoupReplacer( name_xformer=lambda tag: ( "blockquote" if tag.name == "b" else tag.name ) )

        soup = BeautifulSoup( html, "html.parser", replacer=replacer )

        print(soup.prettify())
        blockquote = soup.find("blockquote")

        assert blockquote is not None
        assert blockquote.get_text() == "world"
        assert soup.find("b") is None


    def test_nested_tags_replace_works_w_structure(self):
        new_replacer = SoupReplacer(
            name_xformer=lambda tag: "blockquote" if tag.name=="b" else tag.name
        )
        soup = BeautifulSoup(html_nested, "html.parser",replacer=new_replacer)
        print(soup.prettify())
        blockquote = soup.find_all("blockquote")

        assert len(blockquote) == 2
        assert soup.find("b") is None
        assert blockquote[1].find_parent("blockquote") is blockquote[0]
        p = soup.find("p")
        assert p is not None
        assert p.parent is soup.find("div")
    
    def test_attrs_xformer_works(self):
        html_attrs = '<p class="intro" id="first">Hello</p>'

        def remove_class(tag):
            new_attr = tag.attrs.copy()
            new_attr.pop("class",None)
            return new_attr

        replacer = SoupReplacer(attrs_xformer=remove_class)
        soup = BeautifulSoup(html_attrs, "html.parser", replacer=replacer)

        p = soup.find("p")
        assert p is not None
        assert "class" not in p.attrs
        assert p.get("id") == "first"
        assert p.get_text() == "Hello"

        
    def test_xformer_works(self):
        html_attrs = '<p class="intro" id="first">Hello</p>'

        def remove_class(tag):
            tag.attrs.pop("class", None)

        replacer = SoupReplacer(xformer=remove_class)
        soup = BeautifulSoup(html_attrs, "html.parser", replacer=replacer)

        p = soup.find("p")
        assert p is not None
        assert "class" not in p.attrs
        assert p.get("id") == "first"
        assert p.get_text() == "Hello"

    def test_combined_transformers(self):
        html_combined = '<b class="old" id="first">Hello</b>'

        name_xformer=lambda tag: "blockquote" if tag.name=="b" else tag.name
        def x_class(tag):
            new_attr = tag.attrs.copy()
            new_attr.pop("class", None)
            return new_attr

        replacer = SoupReplacer(
            name_xformer = name_xformer,
            attrs_xformer = x_class
        )

        soup = BeautifulSoup(
            html_combined,
            "html.parser",
            replacer=replacer
        )

        blockquote = soup.find("blockquote")
        assert soup.find("b") is None
        assert blockquote is not None
        assert "class" not in blockquote.attrs
        assert blockquote.get("id") == "first"
        assert blockquote.get_text() == "Hello"


    def test_combined_transformers_and_xformer(self):
            html_combined = '<b class="old" id="first">Hello</b>'

            name_xformer=lambda tag: "blockquote" if tag.name=="b" else tag.name
            def x_class(tag):
                tag.attrs.pop("class", None)

            replacer = SoupReplacer(
                name_xformer = name_xformer,
                xformer = x_class
            )

            soup = BeautifulSoup(
                html_combined,
                "html.parser",
                replacer=replacer
            )

            blockquote = soup.find("blockquote")
            assert soup.find("b") is None
            assert blockquote is not None
            assert "class" not in blockquote.attrs
            assert blockquote.get("id") == "first"
            assert blockquote.get_text() == "Hello"

    def test_no_xformer_work(self):
            original_html = '<b class="old" id="first">Hello</b>'

            original = BeautifulSoup(original_html, "html.parser")

            transformed = BeautifulSoup(
                original_html,
                "html.parser",
                replacer=SoupReplacer()
            )
            assert str(transformed) == str(original)

        
