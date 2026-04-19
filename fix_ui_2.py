import bs4
import re

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove music buttons
soup = bs4.BeautifulSoup(html, 'html.parser')
for cls_name in ['playbgmusic', 'stopbgmusic']:
    elems = soup.find_all(class_=re.compile(cls_name))
    for el in elems:
        el.decompose()

# 2. Remove "Желтоқсан 2025" and the static calendar block that might have it
# Let's search for "Желтоқсан 2025". We want to remove it.
# Actually let's just find the text "Желтоқсан 2025" and replace it with ""
for txt in soup.find_all(string=lambda t: t and 'Желтоқсан 2025' in t):
    txt.replace_with(txt.replace('Желтоқсан 2025', ''))

# It might also say "15:00" which we already changed to "18:00". But there's another block that says "Желтоқсан 2025Күнтізбе".
# Let's just forcibly remove it globally as string replacements in soup don't always catch nested minified nodes.

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup).replace('Желтоқсан 2025', ''))

print("Removed Music and Желтоқсан 2025")
