import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. Remove 23_3.png.webp
# It might be in an <img> tag or a background style, but usually an img
for img in soup.find_all('img'):
    if img.get('src') and '23_3' in img.get('src'):
        img.decompose()
        print('Removed spinning image from img tag')

# It might also be a div background
for div in soup.find_all(True):
    style = div.get('style', '')
    if '23_3' in style:
        div.decompose() # Remove the whole spinning wrapper
        print('Removed spinning image wrapper div')

# 2. Update text to "Серікқали әкемізге 63 жас, Нұргүл анамызға 60 жас"
# The current text might just be "Серікқали" and "Нұргүл" in some blocks.
# I'll search for the elements containing them.
for span in soup.find_all(class_='celebrant-name'):
    text = span.get_text(strip=True)
    if 'Серікқали' in text and 'Нұргүл' not in text:
        span.string = "Серікқали әкемізге 63 жас"
    elif 'Нұргүл' in text:
        span.string = "Нұргүл анамызға 60 жас"
    elif 'Серікқали' in text and 'Нұргүл' in text:
        span.string = "Серікқали әкемізге 63 жас, Нұргүл анамызға 60 жас"

# Just raw HTML replacement if they aren't uniquely classed:
out_html = str(soup)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(out_html)
print("HTML modified")
