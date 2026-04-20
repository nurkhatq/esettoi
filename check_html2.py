import sys
sys.stdout.reconfigure(encoding='utf-8')

import bs4, os, re

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Check where photos section ended up
for kw in ['host-photos', 'gallery/host', 'Серікқали', 'celebrant-name']:
    idx = html.find(kw)
    if idx >= 0:
        snippet = html[max(0,idx-30):idx+80]
        print(f"Found '{kw}' at {idx}")
    else:
        print(f"NOT FOUND: '{kw}'")

# Identify the host portrait paragraph - look for what text is near the "Той иелері" style sections
soup = bs4.BeautifulSoup(html, 'html.parser')

# Search for any div that has gallery images
gallery_divs = soup.find_all('div', id='host-photos')
print(f"\nhost-photos divs: {len(gallery_divs)}")

# Find where celebrant-name or the name text block is
celebrant = soup.find(class_='celebrant-name')
if celebrant:
    print("celebrant-name parent:", celebrant.parent.name, list(celebrant.parent.attrs.keys()))

# Search for the invitee text block
for el in soup.find_all(string=True):
    if 'Серікқали' in el or 'Нұргүл' in el:
        print(f"\nFound name text node in: <{el.parent.name}> class={el.parent.get('class','')}")
        print("  Text:", el[:100])
        break
