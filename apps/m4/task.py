# Set the class attribute of all <p> tags to "test" during parsing.

from bs4 import BeautifulSoup, SoupReplacer
import sys

if len(sys.argv) < 2:
    print("Please provide an HTML file.")
    sys.exit(1)
    
with open(sys.argv[1], "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

for node in soup:
  print(node.name if node.name else str(node))