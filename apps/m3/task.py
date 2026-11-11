# Set the class attribute of all <p> tags to "test" during parsing.

from bs4 import BeautifulSoup, SoupReplacer
import sys

def set_test_class(tag):
    if tag.name == "p":
        tag["class"] = "test"

new_replacer = SoupReplacer(
            xformer=set_test_class
        )
if len(sys.argv) < 2:
    print("Please provide an HTML file.")
    sys.exit(1)
    
with open(sys.argv[1], "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser",replacer=new_replacer)

xformer_soup = soup.prettify()

with open("apps/m3/xformersoup.html","w", encoding="utf-8") as newfile:
    newfile.write(xformer_soup)