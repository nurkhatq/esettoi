import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

target_text = soup.find(string=lambda t: t and 'Құрметті қонақтар!' in t)

if target_text:
    block = target_text.parent
    while block and block.name != 'body':
        if hasattr(block, 'attrs') and 't-rec' in block.get('class', []):
            break
        block = block.parent

    if block and 't-rec' in block.get('class', []):
        parent_container = block.parent
        # filter only Tag elements
        siblings = [s for s in parent_container.children if isinstance(s, bs4.Tag)]
        target_idx = siblings.index(block)
        
        to_remove = []
        for i in range(target_idx):
            sibling = siblings[i]
            if 't-rec' in sibling.get('class', []):
                to_remove.append(sibling)
        
        for r in to_remove:
            r.decompose()
        
        with open('d:/toi/esettoi/public/index.html', 'w', encoding='utf-8') as fout:
            fout.write(str(soup))
        print(f"Successfully removed {len(to_remove)} introductory blocks.")
    else:
        print("Could not find a containing t-rec block.")
else:
    print("Could not find string.")
