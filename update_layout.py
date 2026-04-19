import bs4
import re

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. Fix Audio button positions using CSS injection
css_fix = """
<style>
.playbgmusic, .stopbgmusic {
   position: fixed !important;
   top: 15px !important;
   left: auto !important;
   right: 15px !important;
   z-index: 99999 !important;
   margin: 0 !important;
   transform: none !important;
   width: 40px !important;
   height: 40px !important;
}
</style>
"""
soup.head.append(bs4.BeautifulSoup(css_fix, 'html.parser'))

# Find the old absolutely positioned portrait items and hide them
for div in soup.find_all('div', class_='t-bgimg'):
    style = div.get('style', '')
    if 'host_0.jpg' in style or 'host_1.jpg' in style:
        # Hide the old floating photos because they are unreliably positioned
        if 'display' not in style:
            div['style'] = style + '; display: none !important;'

# 2. Photos over "Той иелері"
toi_ieleri = soup.find(string=lambda t: t and 'Той иелері' in t)
if toi_ieleri:
    # "Той иелері" is located inside a div wrapper. We need to find its parent div to insert the photos.
    parent_div = toi_ieleri.parent
    if parent_div and parent_div.name == 'div':
        photos_html = """
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
           <img src="./assets/gallery/host_0.jpg" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #AD9A6B; padding: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
           <img src="./assets/gallery/host_1.jpg" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #AD9A6B; padding: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </div>
        """
        parent_div.insert_before(bs4.BeautifulSoup(photos_html, 'html.parser'))

# 3. Update Address
qaragandy = soup.find(string=lambda t: t and 'Қарағанды' in t)
if qaragandy:
    qaragandy.replace_with('Ақтөбе')

# 4. Enhance Text
# First find the existing text span or div containing the celebrant string
for el in soup.find_all(string=lambda t: t and 'Серікқали мен Нұргүл' in t):
    el_parent = el.parent
    if el_parent and 'celebrant-name' in el_parent.get('class', []):
        text_container = el_parent.parent
        new_text = """
        Құрметті ағайын-туыс, бауырлар, құда-жекжат, достар!<br><br>
        Сіздерді аяулы әкеміз <span class="celebrant-name" style="font-size: 2.5rem; display: block; margin: 10px 0;">Серікқали</span> 
        және ардақты анамыз <span class="celebrant-name" style="font-size: 2.5rem; display: block; margin: 10px 0;">Нұргүлдің</span> 
        60 жас мерейтойына арналған салтанатты ақ дастарханымыздың қадірлі қонағы болуға шақырамыз!
        """
        text_container.clear()
        text_container.append(bs4.BeautifulSoup(new_text, 'html.parser'))

# 5. Add Wishes (Тілек) textarea to the Form
form = soup.find('form', id='rsvpForm')
if form:
    # Insert before the submit button
    submit_btn = form.find('button', type='submit')
    
    # We replace the entire form inner html to be safe and clean since we manually wrote it earlier
    new_form_content = """
            <input type="text" id="guestName" required placeholder="Аты-жөніңізді жазыңыз" style="padding: 15px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; font-family: inherit; width: 100%; box-sizing: border-box;">
            
            <textarea id="guestWishes" placeholder="Ақ тілегіңізді жазыңыз (міндетті емес)" rows="3" style="padding: 15px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; font-family: inherit; width: 100%; box-sizing: border-box; resize: vertical;"></textarea>

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
    """
    form.clear()
    form.append(bs4.BeautifulSoup(new_form_content, 'html.parser'))
    
    # Update script inside custom-rsvp-form
    script = soup.find('script', string=lambda t: t and 'submitRSVP' in t)
    if script:
        new_script = """
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
                const wishes = document.getElementById('guestWishes') ? document.getElementById('guestWishes').value : '';
                try {
                    await fetch('/api/rsvp', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ name, status, wishes })
                    });
                    document.getElementById('rsvpForm').style.display = 'none';
                    document.getElementById('rsvp-success').style.display = 'block';
                } catch(err) {
                    alert('Қате шықты. Қайта көріңіз.');
                    btn.innerText = 'Жіберу';
                    btn.disabled = false;
                }
            }
        """
        script.string.replace_with(new_script)

with open('d:/toi/esettoi/public/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("HTML UI features updated!")
