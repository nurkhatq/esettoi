import re

html = open('d:/toi/esettoi/public/index.html', encoding='utf-8').read()

imgs = re.findall(r'src="(assets/[^"]+)"', html)
bgs = re.findall(r'background-image:\s*url\(\'(\.\/assets/[^\']+)\'\)', html)
gallery = re.findall(r'gallery/[^"\']+', html)

print("IMG SRCs:")
for i in imgs:
    print(" ", i)
print("\nBG images:")
for b in bgs:
    print(" ", b)
print("\nGallery images:")
for g in gallery:
    print(" ", g)

# Check files exist
import os
print("\nGallery files that exist:")
gdir = 'd:/toi/esettoi/public/assets/gallery'
if os.path.exists(gdir):
    for f in os.listdir(gdir):
        print(" ", f)
