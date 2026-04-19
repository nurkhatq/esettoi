import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

for cls in ['playbgmusic', 'stopbgmusic']:
    for el in soup.find_all(class_=lambda x: x and cls in x):
        el.decompose()

# Remove audio tags just in case
for el in soup.find_all('audio'):
    el.decompose()

out_html = str(soup).replace('Желтоқсан 2025', '')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(out_html)
