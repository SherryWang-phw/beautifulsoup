# Print out all the tags that have an id attribute. (this should be done with a single API call)
from bs4 import BeautifulSoup, SoupStrainer
import sys

only_id = SoupStrainer(id=True)

if len(sys.argv) < 2:
    print("Please provide an HTML file.")
    sys.exit(1)
    
with open(sys.argv[1], "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser",parse_only=only_id)

tags_w_id = soup.find_all(id=True)

for tag in tags_w_id:
    print(tag)
# print(tags_w_id)