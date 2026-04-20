import bs4
html = open('d:/toi/esettoi/public/index.html', encoding='utf-8').read()
soup = bs4.BeautifulSoup(html, 'html.parser')

output = []
for idx, block in enumerate(soup.find_all('div', id=lambda x: x and x.startswith('rec'))):
    b_str = str(block)
    if '31__.png.webp' in b_str:
        output.append(f"31__.png.webp is in {block.get('id')} at block index {idx}")
    if '1748813328120' in b_str or 'field="tn_text_1748813328120"' in b_str:
        output.append(f"Text 1748813328120 is in {block.get('id')} at block index {idx}")
    if 'custom-venue-card' in b_str:
        output.append(f"custom-venue-card is in {block.get('id')} at block index {idx}")
    if 'custom-rsvp-form' in b_str:
        output.append(f"custom-rsvp-form is in {block.get('id')} at block index {idx}")
        
with open('d:/toi/esettoi/debug_moves.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
