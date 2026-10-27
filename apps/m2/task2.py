# Print out all the hyperlinks (<a> tags).
from bs4 import BeautifulSoup, SoupStrainer
import sys

only_links = SoupStrainer("a", href=True)

if len(sys.argv) < 2:
    print("Please provide an HTML file.")
    sys.exit(1)
    
with open(sys.argv[1], "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser", parse_only=only_links)

links = soup.find_all("a")

for link in links:
    print(link.get("href"))