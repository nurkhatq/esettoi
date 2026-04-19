import os
import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace any remaining "13 Желтоқсан" -> "13 Маусым"
html = html.replace('13 Желтоқсан', '13 Маусым')
html = html.replace('27 Желтоқсан', '13 Маусым')

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. Replace circle images at the top
# The circle images are divs with specific tildacdn background styles
for div in soup.find_all('div', class_='t-bgimg'):
    style = div.get('style', '')
    if 'tild3736-3532-4465-b161-646236653239/2.png' in style or 'tild3135-3131-4134-b139-313164376165/1.png' in style:
        # It's one of the circle portraits. Let's just point them to host_0 and host_1
        # Actually to be safe, any cover background that has "tildacdn" we can map to our hosts
        if '2.png' in style:
            div['style'] = "background-image: url('./assets/gallery/host_0.jpg');"
            div['data-original'] = "./assets/gallery/host_0.jpg"
        else:
            div['style'] = "background-image: url('./assets/gallery/host_1.jpg');"
            div['data-original'] = "./assets/gallery/host_1.jpg"

    if '____________________.jpeg' in style:
        # replace the main background hero image with host_2
        div['style'] = "background-image: url('./assets/gallery/host_2.jpg');"
        div['data-original'] = "./assets/gallery/host_2.jpg"

for img in soup.find_all('img'):
    src = img.get('src', '')
    if '____________________.jpeg' in src:
        img['src'] = './assets/gallery/host_2.jpg'
        img['data-original'] = './assets/gallery/host_2.jpg'

# 2. Add an Image Gallery block before the RSVP form.
# The RSVP form is around "Төмендегі сауалнаманы толтырып, келуіңізді растаңыз"
rsvp_title = soup.find(string=lambda t: t and 'сауалнаманы толтырып' in t)
if rsvp_title:
    # Go up to the block level
    rsvp_block = rsvp_title.parent
    for _ in range(5):
        if rsvp_block.name == 'div' and ('r' in rsvp_block.get('class', []) or 't-rec' in rsvp_block.get('class', [])):
            break
        if rsvp_block.parent:
            rsvp_block = rsvp_block.parent

    # Insert a nice flexbox gallery before the rsvp_block
    gallery_html = """
    <div id="custom-gallery" style="padding: 40px 10px; text-align: center;">
        <h2 style="color: #AD9A6B; font-family: 'KZAstanaPro-Medium', serif; font-size: 24px; margin-bottom: 20px;">Фотогалерея</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
            <img src="./assets/gallery/host_0.jpg" style="width: 48%; border-radius: 12px; object-fit: cover; aspect-ratio: 4/5; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <img src="./assets/gallery/host_1.jpg" style="width: 48%; border-radius: 12px; object-fit: cover; aspect-ratio: 4/5; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <img src="./assets/gallery/host_3.jpg" style="width: 48%; border-radius: 12px; object-fit: cover; aspect-ratio: 4/5; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <img src="./assets/gallery/host_4.jpg" style="width: 48%; border-radius: 12px; object-fit: cover; aspect-ratio: 4/5; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <img src="./assets/gallery/host_2.jpg" style="width: 98%; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 5px;">
        </div>
    </div>
    """
    new_gallery = bs4.BeautifulSoup(gallery_html, 'html.parser')
    rsvp_block.insert_before(new_gallery)

# 3. Create the RSVP Form
# Find the Келемін and Келе алмаймын buttons
# "Келемін", "Келе алмаймын"
kelemin_btn = soup.find(string=lambda t: t and 'Келемін' in t)
if kelemin_btn:
    form_html = """
    <div id="custom-rsvp-form" style="max-width: 420px; margin: 0 auto; padding: 20px; background: white; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.05); border: 1px solid #f5f3ed;">
        <div id="rsvp-success" style="display:none; color: #AD9A6B; font-size: 20px; text-align: center; margin-bottom: 20px;">Жауабыңызға рахмет!</div>
        <form id="rsvpForm" onsubmit="submitRSVP(event)" style="display:flex; flex-direction:column; gap: 15px;">
            <input type="text" id="guestName" required placeholder="Аты-жөніңізді жазыңыз" style="padding: 15px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; font-family: inherit;">
            <div style="display: flex; gap: 10px;">
                <label style="flex:1; cursor:pointer; text-align:center; padding: 15px 5px; border-radius: 8px; border: 1px solid #AD9A6B; color: #AD9A6B;">
                    <input type="radio" name="attendance" value="Келемін" required style="display:none;" onchange="updateRadio(this)">
                    Келемін
                </label>
                <label style="flex:1; cursor:pointer; text-align:center; padding: 15px 5px; border-radius: 8px; border: 1px solid #AD9A6B; color: #AD9A6B;">
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
    # Let's replace the whole parent block of the old Tilda buttons with our custom form!
    kelemin_block = kelemin_btn.parent
    for _ in range(5):
        if kelemin_block.name == 'div' and ('r' in kelemin_block.get('class', []) or 't-rec' in kelemin_block.get('class', [])):
            break
        if kelemin_block.parent:
            kelemin_block = kelemin_block.parent
    
    new_form = bs4.BeautifulSoup(form_html, 'html.parser')
    kelemin_block.replace_with(new_form)

open('d:/toi/esettoi/public/index.html', 'w', encoding='utf-8').write(str(soup))
print("Gallery and Form injected successfully.")
