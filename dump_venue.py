import bs4
html = open('d:/toi/esettoi/public/index.html', encoding='utf-8').read()
soup = bs4.BeautifulSoup(html, 'html.parser')
b = soup.find('div', id='rec1521141141')
if b:
    with open('d:/toi/esettoi/debug_venue.html', 'w', encoding='utf-8') as f:
        f.write(str(b))
