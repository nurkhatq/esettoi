import bs4, os, re, shutil
from PIL import Image

html_path = 'd:/toi/esettoi/public/index.html'
assets_dir = 'd:/toi/esettoi/public/assets'
gallery_dir = 'd:/toi/esettoi/public/assets/gallery'

# ─── 1. FIX NUMBER 6 HOLE ───────────────────────────────────────────────────
print("Fixing number 6 hole (strict tolerance)...")
from collections import deque

input_path = 'd:/toi/i.webp'
output_path = os.path.join(assets_dir, 'number_6.png')

img = Image.open(input_path).convert("RGBA")
pixdata = img.load()
width, height = img.size

def is_bg(r, g, b, tolerance=10):
    return r >= 245 and g >= 245 and b >= 245  # Very strict: only near-pure-white

visited = set()
queue = deque()
for x in range(width):
    for y in [0, height - 1]:
        px = pixdata[x, y]
        if (x, y) not in visited and is_bg(*px[:3]):
            queue.append((x, y)); visited.add((x, y))
for y in range(height):
    for x in [0, width - 1]:
        px = pixdata[x, y]
        if (x, y) not in visited and is_bg(*px[:3]):
            queue.append((x, y)); visited.add((x, y))

while queue:
    cx, cy = queue.popleft()
    for nx, ny in [(cx-1,cy),(cx+1,cy),(cx,cy-1),(cx,cy+1)]:
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
            px = pixdata[nx, ny]
            if is_bg(*px[:3]):
                visited.add((nx, ny)); queue.append((nx, ny))

for (x, y) in visited:
    pixdata[x, y] = (0, 0, 0, 0)

img.save(output_path, "PNG")
shutil.copy(output_path, os.path.join(assets_dir, '20_5.png'))
print(f"  Fixed! {len(visited)} px transparent.")

# ─── 2. FIX MISSING WEBP FILES ───────────────────────────────────────────────
print("\nFixing missing .webp files...")
missing_webps = [
    '23_3.png.webp',
]
for fname in os.listdir(assets_dir):
    if fname.endswith('.png.webp'):
        webp_path = os.path.join(assets_dir, fname)
        if not os.path.exists(webp_path):
            png_path = os.path.join(assets_dir, fname.replace('.webp', ''))
            if os.path.exists(png_path):
                shutil.copy(png_path, webp_path)
                print(f"  Restored {fname} from png")

# ─── 3. INJECT PHOTOS + STYLED IMPROVEMENTS ──────────────────────────────────
print("\nUpdating HTML with photos and improved styling...")
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# Find "Той иелері" text and inject photos right before that container
toi_ieleri_el = soup.find(string=lambda t: t and 'Той иелері' in t)
if toi_ieleri_el:
    block = toi_ieleri_el.parent
    # Go up until we find a block-level container with multiple siblings
    for _ in range(6):
        if block.parent and len(list(block.parent.children)) > 2:
            break
        block = block.parent

    # Build gallery of all 5 photos
    photos_html = """
<div id="host-photos" style="padding: 30px 15px 10px; background: linear-gradient(to bottom, transparent, rgba(255,248,235,0.5));">
  <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; max-width:420px; margin:0 auto;">
    <div style="width:120px; height:150px; overflow:hidden; border-radius:12px; box-shadow:0 6px 20px rgba(173,154,107,0.3); border:2px solid rgba(173,154,107,0.5);">
      <img src="assets/gallery/host_0.jpg" style="width:100%; height:100%; object-fit:cover; object-position:top;">
    </div>
    <div style="width:120px; height:150px; overflow:hidden; border-radius:12px; box-shadow:0 6px 20px rgba(173,154,107,0.3); border:2px solid rgba(173,154,107,0.5);">
      <img src="assets/gallery/host_1.jpg" style="width:100%; height:100%; object-fit:cover; object-position:top;">
    </div>
    <div style="width:120px; height:150px; overflow:hidden; border-radius:12px; box-shadow:0 6px 20px rgba(173,154,107,0.3); border:2px solid rgba(173,154,107,0.5);">
      <img src="assets/gallery/host_2.jpg" style="width:100%; height:100%; object-fit:cover; object-position:top;">
    </div>
  </div>
  <div style="display:flex; justify-content:center; gap:12px; margin-top:12px; max-width:420px; margin-left:auto; margin-right:auto;">
    <div style="width:190px; height:140px; overflow:hidden; border-radius:12px; box-shadow:0 6px 20px rgba(173,154,107,0.3); border:2px solid rgba(173,154,107,0.5);">
      <img src="assets/gallery/host_3.jpg" style="width:100%; height:100%; object-fit:cover; object-position:top;">
    </div>
    <div style="width:190px; height:140px; overflow:hidden; border-radius:12px; box-shadow:0 6px 20px rgba(173,154,107,0.3); border:2px solid rgba(173,154,107,0.5);">
      <img src="assets/gallery/host_4.jpg" style="width:100%; height:100%; object-fit:cover; object-position:top;">
    </div>
  </div>
</div>
"""
    # Only inject if not already there
    if not soup.find('div', id='host-photos'):
        block.insert_before(bs4.BeautifulSoup(photos_html, 'html.parser'))
        print("  Injected host photos before Той иелері block")

# ─── 4. GLOBAL STYLE POLISH ───────────────────────────────────────────────────
style_injection = """
<style>
/* ── General polish ── */
body { -webkit-font-smoothing: antialiased; }

/* ── Countdown timer ── */
#custom-timer-container {
  background: linear-gradient(135deg, rgba(255,248,235,0.95), rgba(255,238,210,0.85));
  border-radius: 20px;
  margin: 0 15px;
  padding: 35px 20px !important;
  box-shadow: 0 8px 30px rgba(173,154,107,0.2);
  border: 1px solid rgba(173,154,107,0.25);
}
#countdown-timer > div span:first-child {
  font-weight: 800 !important;
  letter-spacing: -1px;
  border-radius: 12px !important;
  background: linear-gradient(135deg, rgba(173,154,107,0.15), rgba(173,154,107,0.08)) !important;
  box-shadow: 0 4px 12px rgba(173,154,107,0.2), inset 0 1px 0 rgba(255,255,255,0.8);
  min-width: 72px !important;
  font-size: 38px !important;
}

/* ── RSVP Form ── */
#custom-rsvp-form {
  border-radius: 20px !important;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08) !important;
  border: 1px solid rgba(173,154,107,0.2) !important;
  background: linear-gradient(to bottom, #fff, #fffdf8) !important;
  margin: 0 15px !important;
}
#custom-rsvp-form button[type="submit"] {
  border-radius: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px;
  background: linear-gradient(135deg, #c9a96e, #AD9A6B) !important;
  box-shadow: 0 6px 20px rgba(173,154,107,0.4) !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
}
#custom-rsvp-form button[type="submit"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(173,154,107,0.5) !important;
}
#custom-rsvp-form input[type="text"],
#custom-rsvp-form textarea {
  border-radius: 10px !important;
  border-color: rgba(173,154,107,0.3) !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
#custom-rsvp-form input:focus,
#custom-rsvp-form textarea:focus {
  outline: none;
  border-color: #AD9A6B !important;
  box-shadow: 0 0 0 3px rgba(173,154,107,0.15);
}

/* ── Host Photos ── */
#host-photos img {
  transition: transform 0.3s;
}
#host-photos img:hover {
  transform: scale(1.05);
}
</style>
"""

# Only add once
if 'custom-rsvp-form' in str(soup) and '── General polish ──' not in str(soup):
    soup.head.append(bs4.BeautifulSoup(style_injection, 'html.parser'))
    print("  Injected global style polish")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("\nAll done!")
