import bs4
import re

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# TEXT REPLACEMENTS USING REGEX FOR EXACT TEXT NODES
html = html.replace('27 Желтоқсан 2025', '13 Маусым 2026')
html = html.replace('27 Желтоқсан', '13 Маусым')
html = re.sub(r'27(?=\s*<)', '13', html)
html = html.replace('15:00', '18:00')
html = html.replace('Ресторан "ARISTA"', 'Патша')
html = html.replace('Микрорайон Восток 3, 17/1', '')
html = html.replace('https://2gis.com/9KLUM', 'https://2gis.kz/aktobe/geo/70000001032511581')
# The text line replacement: "Сіз(дер)ді Алмастың әкемиз 50 жас мерей тойына..."
html = html.replace(
    '<span class="celebrant-name">Алмастың</span> әкемиз 50 жас мерей тойына',
    '<span class="celebrant-name" style="font-size: 2.2rem;">Серікқали мен Нұргүл</span> 60 жас мерей тойына'
)

soup = bs4.BeautifulSoup(html, 'html.parser')

# REPLACE THE TWO CIRCULAR PORTRAITS ONLY
for div in soup.find_all('div', class_='t-bgimg'):
    style = div.get('style', '')
    # The two small circular portraits are "2.png" and "1.png" in specific paths
    if 'tild3736-3532-4465-b161-646236653239/2.png' in style:
        div['style'] = "background-image: url('./assets/gallery/host_0.jpg');"
        div['data-original'] = "./assets/gallery/host_0.jpg"
    elif 'tild3135-3131-4134-b139-313164376165/1.png' in style:
        div['style'] = "background-image: url('./assets/gallery/host_1.jpg');"
        div['data-original'] = "./assets/gallery/host_1.jpg"

    # For the background "5" image (tild3665-6335-4736-b065-623430306236/3.png) we DON'T touch since user wanted its appearance to be retained except for replacing the "5". 
    # That "5" is replaced manually via `shutil.copy(i.webp -> 20_5.png)` earlier ! Wait, 20_5.png is the 5!

# INJECT RSVP FORM
kelemin_btn = soup.find(string=lambda t: t and 'Келемін' in t)
if kelemin_btn:
    form_html = """
    <div id="custom-rsvp-form" style="max-width: 420px; margin: 0 auto; padding: 20px; background: white; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.05); border: 1px solid #f5f3ed;">
        <div id="rsvp-success" style="display:none; color: #AD9A6B; font-size: 20px; text-align: center; margin-bottom: 20px;">Жауабыңызға рахмет!</div>
        <form id="rsvpForm" onsubmit="submitRSVP(event)" style="display:flex; flex-direction:column; gap: 15px;">
            <input type="text" id="guestName" required placeholder="Аты-жөніңізді жазыңыз" style="padding: 15px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; font-family: inherit; width: 100%; box-sizing: border-box;">
            <div style="display: flex; gap: 10px;">
                <label style="flex:1; cursor:pointer; text-align:center; padding: 15px 5px; border-radius: 8px; border: 1px solid #AD9A6B; color: #AD9A6B; font-size: 14px;">
                    <input type="radio" name="attendance" value="Келемін" required style="display:none;" onchange="updateRadio(this)">
                    Келемін
                </label>
                <label style="flex:1; cursor:pointer; text-align:center; padding: 15px 5px; border-radius: 8px; border: 1px solid #AD9A6B; color: #AD9A6B; font-size: 14px;">
                    <input type="radio" name="attendance" value="Келе алмаймын" required style="display:none;" onchange="updateRadio(this)">
                    Келе алмаймын
                </label>
            </div>
            <button type="submit" style="margin-top: 10px; padding: 15px; background: #AD9A6B; color: white; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 12px rgba(173,154,107,0.3);">Жіберу</button>
        </form>
        <style>
            input[type="radio"]:checked + label, label:has(input[type="radio"]:checked) {
                background-color: #AD9A6B !important;
                color: white !important;
            }
        </style>
        <script>
            function updateRadio(radio) {
                let labels = radio.closest('form').querySelectorAll('label');
                labels.forEach(l => {
                    l.style.background = 'transparent';
                    l.style.color = '#AD9A6B';
                });
                radio.closest('label').style.background = '#AD9A6B';
                radio.closest('label').style.color = 'white';
            }
            async function submitRSVP(e) {
                e.preventDefault();
                const btn = e.target.querySelector('button');
                btn.innerText = 'Күте тұрыңыз...';
                btn.disabled = true;
                const name = document.getElementById('guestName').value;
                const status = document.querySelector('input[name="attendance"]:checked').value;
                try {
                    await fetch('/api/rsvp', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ name, status })
                    });
                    document.getElementById('rsvpForm').style.display = 'none';
                    document.getElementById('rsvp-success').style.display = 'block';
                } catch(err) {
                    alert('Қате шықты. Қайта көріңіз.');
                    btn.innerText = 'Жіберу';
                    btn.disabled = false;
                }
            }
        </script>
    </div>
    """
    kelemin_block = kelemin_btn.parent
    for _ in range(5):
        if kelemin_block.name == 'div' and ('r' in kelemin_block.get('class', []) or 't-rec' in kelemin_block.get('class', [])):
            break
        if kelemin_block.parent:
            kelemin_block = kelemin_block.parent
    
    new_form = bs4.BeautifulSoup(form_html, 'html.parser')
    kelemin_block.replace_with(new_form)

open('d:/toi/esettoi/public/index.html', 'w', encoding='utf-8').write(str(soup))
print("Form injected and text updated without extra galleries.")
