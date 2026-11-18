from bs4 import BeautifulSoup

def test_soup_iteration_nested():
    html = "<div><p>Hello</p></div>"
    soup = BeautifulSoup(html, "html.parser")

    nodes = []
    for node in soup:
        nodes.append(node.name if node.name else str(node))

    assert nodes == ["div", "p", "Hello"]


def test_soup_iteration_empty():
    html = ""
    soup = BeautifulSoup(html, "html.parser")

    nodes = []
    for node in soup:
        nodes.append(node.name if node.name else str(node))

    assert len(list(soup)) == 0

def test_soup_iteration_multiple_siblings():
    html = "<div><p>One</p><p>Two</p></div>"
    soup = BeautifulSoup(html, "html.parser")

    nodes = []
    for node in soup:
        nodes.append(node.name if node.name else str(node))

    assert nodes == ["div", "p", "One", "p", "Two"]

def test_soup_iteration_mixed_node_types():
    html = "<div>Hello<!-- comment --><b>World</b></div>"
    soup = BeautifulSoup(html, "html.parser")

    nodes = []
    for node in soup:
        nodes.append(node.name if node.name else str(node))

    assert nodes == ["div", "Hello", " comment ", "b", "World"]

def test_soup_iteration_repeat():
    html = "<div>Hello<!-- comment --><b>World</b></div>"
    soup = BeautifulSoup(html, "html.parser")

    first = [str(node) for node in soup]
    second = [str(node) for node in soup]

    assert first == second