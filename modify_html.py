import os
import re
import shutil

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Text Replacements
replacements = {
    '27': '13',
    'Желтоқсан 2025': 'Маусым 2026',
    '15:00': '18:00',
    'Ресторан "ARISTA"': 'Патша',
    'Микрорайон Восток 3, 17/1': ' ',
    'https://2gis.com/9KLUM': 'https://2gis.kz/aktobe/geo/70000001032511581'
}

# The number 27 appears frequently, we want to replace only the visual text
# So we'll use regex for exact matches in HTML >...<
html = re.sub(r'27(?=\s*<| Жел)', '13', html)
html = html.replace('Желтоқсан 2025', 'Маусым 2026')
html = html.replace('15:00', '18:00')
html = html.replace('Ресторан "ARISTA"', 'Патша')
html = html.replace('Микрорайон Восток 3, 17/1', '')
html = html.replace('https://2gis.com/9KLUM', 'https://2gis.kz/aktobe/geo/70000001032511581')

# 2. Image Replacements
# We have 5 host images. We need to find the background-images or img src that show people.
# The template has two small circle images at the top (host parents) 
# Wait, the user said "для той иелери" (for the hosts). Let's copy all images.
images_dir = 'd:/toi/images'
dest_dir = 'd:/toi/esettoi/public/assets/new_images'
os.makedirs(dest_dir, exist_ok=True)

user_images = os.listdir(images_dir)
# Let's say we just want to replace all tildacdn.com image backgrounds/src that look like people realistically
# Let's see the unique tildacdn.com usages.
urls = re.findall(r'(https://[^\'"]+tildacdn\.com[^\'"]+\.(?:jpg|png|webp))', html)
unique_urls = list(set(urls))

# We'll just print them and we'll manually replace them in the next step, since we need to see what they are.
print("Found Tilda URLs:")
for u in unique_urls:
    print(u)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Finished basic text replacement.")
