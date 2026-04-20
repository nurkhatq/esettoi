import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

target = '<div id="custom-venue-card"'

replacement = """<div id="hosts-info" style="margin: 0px 15px 20px; padding: 20px; background: transparent; text-align: center;">
<h3 style="font-family: inherit; color: #AD9A6B; font-size: 20px; margin-bottom: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px;">Той иелері:</h3>
<div style="font-family: 'KZAstanaPro-Medium', serif; font-size: 36px; color: #8d5437; line-height: 1.4; margin-bottom: 15px;">
Серікқали - Нұргүл
</div>
<div style="font-family: inherit; font-size: 20px; color: #555; text-transform: uppercase; letter-spacing: 1px;">
Балалары
</div>
</div>
<div id="custom-venue-card" """

if target in html:
    html = html.replace(target, replacement)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Hosts block added successfully.")
else:
    print("Target venue card not found.")
