# Print out all the tags in the document.
from bs4 import BeautifulSoup, SoupStrainer
import sys

only_tags = SoupStrainer(True)

if len(sys.argv) < 2:
    print("Please provide an HTML file.")
    sys.exit(1)
    
with open(sys.argv[1], "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser", parse_only=only_tags)

tags = soup.find_all(True)

for tag in tags:
    print(tag)