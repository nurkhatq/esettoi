import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# Find the host-photos container
container = soup.find(id='host-photos')
if container:
    # Find all divs that are immediate children of the inner flex containers
    # The last two images are host_3.jpg and host_4.jpg
    for img in container.find_all('img'):
        src = img.get('src')
        if src in ['assets/gallery/host_3.jpg', 'assets/gallery/host_4.jpg']:
            # Grab the parent div which controls the height
            parent_div = img.parent
            style = parent_div.get('style', '')
            # Replace height:130px with height:220px
            style = style.replace('height:130px', 'height:240px')
            # You can also change the width if necessary to keep them nice
            parent_div['style'] = style
            
            # Change object-position
            img_style = img.get('style', '')
            img_style = img_style.replace('object-position:top', 'object-position:center 20%')
            img['style'] = img_style
        elif src in ['assets/gallery/host_0.jpg', 'assets/gallery/host_1.jpg', 'assets/gallery/host_2.jpg']:
            img_style = img.get('style', '')
            img_style = img_style.replace('object-position:top', 'object-position:center 20%')
            img['style'] = img_style

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Fixed photo cropping")
