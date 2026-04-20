import bs4

html = open('d:/toi/esettoi/public/index.html', encoding='utf-8').read()
soup = bs4.BeautifulSoup(html, 'html.parser')

output = []
for t in soup.find_all(string=True):
    if 'Ақтөбе' in t:
        output.append(f"Found 'Ақтөбе' in block: <{t.parent.name}>")
        output.append(f"Parent: {t.parent.parent.name} | Text: {t.parent.parent.text[:100].strip()}")
        # Write some surroundings
        idx = html.find('Ақтөбе')
        output.append(f"Raw HTML chunk: {html[max(0, idx-300):idx+300]}")
        break

with open('d:/toi/esettoi/context.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
