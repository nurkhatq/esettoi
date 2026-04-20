import sys
sys.stdout.reconfigure(encoding='utf-8')

import bs4, os

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# ──────────────────────────────────────────────
# 1. Remove old broken host-photos block (if any)
# ──────────────────────────────────────────────
for old in soup.find_all(id='host-photos'):
    old.decompose()
print("Cleaned old host-photos blocks")

# ──────────────────────────────────────────────
# 2. Find the "Серікқали" span (celebrant-name)
#    and walk up to a t-rec level container to inject before it
# ──────────────────────────────────────────────
seri = soup.find('span', class_='celebrant-name')
if seri:
    block = seri
    # Walk up until we find a div with class containing 't-rec'
    for _ in range(10):
        p = block.parent
        if p is None:
            break
        cls = ' '.join(p.get('class', []))
        if 't-rec' in cls or 'tn-elem' in cls:
            break
        block = p
    
    # block is now the section containing the celebrant name
    # We will insert photos BEFORE this block
    photos_html = """
<div id="host-photos" style="padding:25px 15px 5px; text-align:center;">
  <div style="display:flex; justify-content:center; gap:10px; max-width:400px; margin:0 auto 10px;">
    <div style="flex:1; max-width:120px; height:155px; overflow:hidden; border-radius:14px; box-shadow:0 6px 18px rgba(173,154,107,0.35); border:2.5px solid rgba(173,154,107,0.6);">
      <img src="assets/gallery/host_0.jpg" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block;">
    </div>
    <div style="flex:1; max-width:120px; height:155px; overflow:hidden; border-radius:14px; box-shadow:0 6px 18px rgba(173,154,107,0.35); border:2.5px solid rgba(173,154,107,0.6);">
      <img src="assets/gallery/host_1.jpg" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block;">
    </div>
    <div style="flex:1; max-width:120px; height:155px; overflow:hidden; border-radius:14px; box-shadow:0 6px 18px rgba(173,154,107,0.35); border:2.5px solid rgba(173,154,107,0.6);">
      <img src="assets/gallery/host_2.jpg" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block;">
    </div>
  </div>
  <div style="display:flex; justify-content:center; gap:10px; max-width:400px; margin:0 auto;">
    <div style="flex:1; max-width:190px; height:130px; overflow:hidden; border-radius:14px; box-shadow:0 6px 18px rgba(173,154,107,0.35); border:2.5px solid rgba(173,154,107,0.6);">
      <img src="assets/gallery/host_3.jpg" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block;">
    </div>
    <div style="flex:1; max-width:190px; height:130px; overflow:hidden; border-radius:14px; box-shadow:0 6px 18px rgba(173,154,107,0.35); border:2.5px solid rgba(173,154,107,0.6);">
      <img src="assets/gallery/host_4.jpg" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block;">
    </div>
  </div>
</div>
"""
    block.insert_before(bs4.BeautifulSoup(photos_html, 'html.parser'))
    print(f"Injected photos before block: <{block.name} class='{' '.join(block.get('class',[])[:3])}'>")
else:
    print("ERROR: celebrant-name span not found!")

# ──────────────────────────────────────────────
# 3. Inject final CSS polish
# ──────────────────────────────────────────────
css = """
<style id="custom-polish">
#host-photos img { transition: transform 0.3s ease; }
#host-photos img:hover { transform: scale(1.04); }

#custom-timer-container {
  background: linear-gradient(135deg, #fffdf5, #fff8e8) !important;
  border-radius: 20px;
  margin: 10px 15px;
  box-shadow: 0 6px 24px rgba(173,154,107,0.18);
  border: 1px solid rgba(173,154,107,0.22) !important;
}
#countdown-timer > div > span:first-child {
  font-weight: 800 !important;
  min-width: 68px !important;
  font-size: 36px !important;
  border-radius: 12px !important;
  background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(255,248,230,0.6)) !important;
  box-shadow: 0 4px 12px rgba(173,154,107,0.18), inset 0 1px 0 rgba(255,255,255,0.9) !important;
}

#custom-rsvp-form {
  border-radius: 20px !important;
  background: linear-gradient(to bottom, #ffffff, #fffdf8) !important;
  box-shadow: 0 12px 40px rgba(0,0,0,0.07) !important;
  border: 1px solid rgba(173,154,107,0.18) !important;
  margin: 10px 15px !important;
}
#custom-rsvp-form input[type="text"],
#custom-rsvp-form textarea {
  border-radius: 10px !important;
  border: 1.5px solid rgba(173,154,107,0.3) !important;
}
#custom-rsvp-form input:focus,
#custom-rsvp-form textarea:focus {
  outline: none !important;
  border-color: #AD9A6B !important;
  box-shadow: 0 0 0 3px rgba(173,154,107,0.12) !important;
}
#custom-rsvp-form button[type="submit"] {
  border-radius: 12px !important;
  font-weight: 700 !important;
  background: linear-gradient(135deg, #c9a96e, #9d8552) !important;
  box-shadow: 0 6px 20px rgba(173,154,107,0.38) !important;
  transition: all 0.25s ease !important;
  letter-spacing: 0.5px !important;
}
#custom-rsvp-form button[type="submit"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 26px rgba(173,154,107,0.48) !important;
}
</style>
"""

# Remove old polish and add fresh
old_style = soup.find('style', id='custom-polish')
if old_style:
    old_style.decompose()
soup.head.append(bs4.BeautifulSoup(css, 'html.parser'))
print("Injected polish CSS")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Done!")
