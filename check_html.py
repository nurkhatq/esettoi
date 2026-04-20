import bs4, os

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Print sections that contain keywords
import re
# Find where "Той иелері" lives - it was replaced/renamed in earlier scripts
# Search for common Kazakhs strings
for kw in ['host-photos', 'gallery/host', 'Той иелер', 'celebrant-name', 'Сері', 'Нұрг']:
    idx = html.find(kw)
    if idx >= 0:
        snippet = html[max(0,idx-30):idx+80]
        print(f"Found '{kw}' at {idx}: {repr(snippet[:100])}")
    else:
        print(f"NOT FOUND: '{kw}'")
