import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. Update the host-photos gallery to ONLY show host_3.jpg nicely
host_photos = soup.find(id='host-photos')
if host_photos:
    single_photo_html = """
    <div id="host-photos" style="padding:25px 15px 5px; text-align:center;">
      <div style="max-width:320px; height:400px; margin:0 auto; overflow:hidden; border-radius:18px; box-shadow:0 12px 30px rgba(173,154,107,0.4); border:3px solid rgba(173,154,107,0.6);">
        <img src="assets/gallery/host_3.jpg" style="width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block;transition: transform 0.3s ease;">
      </div>
    </div>
    """
    host_photos.replace_with(bs4.BeautifulSoup(single_photo_html, 'html.parser'))
    print("Updated photo gallery to single photo")

# 2. Add venue card before the RSVP form
venue_card_html = """
<div id="custom-venue-card" style="margin: 40px 15px; padding: 40px 20px; background: linear-gradient(135deg, #fffdf8, #ffffff); border-radius: 20px; box-shadow: 0 12px 40px rgba(173,154,107,0.15); border: 1px solid rgba(173,154,107,0.25); text-align: center;">
  <h2 style="font-family: inherit; color: #AD9A6B; font-size: 28px; margin-bottom: 20px; font-weight: bold;">Той өтетін орын</h2>
  
  <div style="font-family: sans-serif; font-size: 18px; color: #444; line-height: 1.6; margin-bottom: 30px;">
    <strong>Ақтөбе қаласы</strong><br/>
    Кунаева көшесі, 1/5<br/>
    <span style="font-size: 24px; font-weight: 800; color: #AD9A6B; display: block; margin-top: 10px;">"Патша" мейрамханасы</span>
  </div>
  
  <a href="https://2gis.kz/aktobe/geo/70000001032511581" target="_blank" style="display: inline-block; padding: 15px 35px; background: linear-gradient(135deg, #c9a96e, #9d8552); color: #fff; text-decoration: none; border-radius: 12px; font-weight: bold; font-family: sans-serif; font-size: 16px; box-shadow: 0 6px 20px rgba(173,154,107,0.4); transition: transform 0.2s;">
    📍 2GIS арқылы ашу
  </a>
</div>
"""
# If it already exists, replace it, otherwise insert before custom-rsvp-form
existing_venue = soup.find(id='custom-venue-card')
if existing_venue:
    existing_venue.replace_with(bs4.BeautifulSoup(venue_card_html, 'html.parser'))
    print("Replaced existing venue card")
else:
    rsvp_form = soup.find(id='custom-rsvp-form')
    if rsvp_form:
        rsvp_form.insert_before(bs4.BeautifulSoup(venue_card_html, 'html.parser'))
        print("Injected venue card before RSVP form")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Finished updates.")
