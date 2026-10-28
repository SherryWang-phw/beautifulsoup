# Change all the <b> tags to <blockquote> tags and write the tree onto a file.
from bs4 import BeautifulSoup, SoupReplacer
import sys

replacer = SoupReplacer("b", "blockquote")
if len(sys.argv) < 2:
    print("Please provide an HTML file.")
    sys.exit(1)
    
with open(sys.argv[1], "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser",replacer=replacer)

b_to_blockquote = soup.prettify()

with open("newblockquotesoup.html","w", encoding="utf-8") as newfile:
    newfile.write(b_to_blockquote)