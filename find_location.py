import bs4
html = open('d:/toi/esettoi/public/index.html', encoding='utf-8').read()
soup = bs4.BeautifulSoup(html, 'html.parser')

output = ""
for div in soup.find_all('div'):
    if 'id' in div.attrs and str(div['id']).startswith('rec'):
        text = div.get_text(' ', strip=True)
        if 'Кунаева' in text or 'Той иелері' in text or 'Мекен-жайымыз' in text or 'Патша' in text or 'карта' in text:
            output += div['id'] + " --> " + text[:100] + "\n"

with open('d:/toi/esettoi/debug_location.txt', 'w', encoding='utf-8') as f:
    f.write(output)
