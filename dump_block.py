import bs4

html = open('d:/toi/esettoi/public/index.html', encoding='utf-8').read()
soup = bs4.BeautifulSoup(html, 'html.parser')

block = soup.find('div', id='rec1080360956')
if block:
    output = str(block)
    # also checking location blocks
else:
    output = "Block 1080360956 not found"

with open('d:/toi/esettoi/debug_block.html', 'w', encoding='utf-8') as f:
    f.write(output)
