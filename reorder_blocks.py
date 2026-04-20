import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. We want to move block `rec1080360956` (Kelininder image) to be between custom-venue-card and custom-rsvp-form.
# But wait, rec1080360956 is a Full Tilda Block `.r.t-rec`. It is usually a direct child of `#allrecords`.
# If we put a `.r.t-rec` INSIDE another `.r.t-rec` (like `rec1521141141`), it might break Tilda's grid.
# The safest way is to split `rec1521141141` into two blocks, OR pull `#custom-venue-card` out of it and make it a block.
# Actually, `#custom-venue-card` and `#hosts-info` are just a few divs. We can create a new `.r.t-rec` block for them and insert it ABOVE `rec1080360956`.

# Let's see:
hosts_info = soup.find('div', id='hosts-info')
venue_card = soup.find('div', id='custom-venue-card')
rsvp_form = soup.find('div', id='custom-rsvp-form')

block_956 = soup.find('div', id='rec1080360956') # Image "Келіңіздер..."
block_936 = soup.find('div', id='rec1080360936') # Text "Төмендегі сауалнаманы..."
block_rsvp = soup.find('div', id='rec1521141141')

if block_956 and block_936 and block_rsvp and hosts_info and venue_card:
    # Instead of breaking tilda nesting, we will rearrange the top-level `.r.t-rec` blocks!
    # Currently `block_rsvp` contains hosts, venue, and form.
    # I will pull out `hosts_info` and `venue_card` and put them in a NEW top-level block.
    
    new_venue_block_html = f'''
    <div class="r t-rec" style="padding: 0; margin: 0;">
       <div class="t123">
         <div class="t-container_100">
           <div class="t-width t-width_100">
             <div class="rsvp-form-wrapper" style="width: 100%; max-width: 1000px; margin: 0px auto; padding: 0px; box-sizing: border-box;">
               {str(hosts_info)}
               {str(venue_card)}
             </div>
           </div>
         </div>
       </div>
    </div>
    '''
    
    # parse the new block
    new_venue_block = bs4.BeautifulSoup(new_venue_block_html, 'html.parser').div
    
    # Now remove them from `block_rsvp`
    hosts_info.extract()
    venue_card.extract()
    
    # We want the order to be:
    # 1. New Venue Block (hosts + venue)
    # 2. block_956 ("Келіңіздер... image")
    # 3. block_936 ("Төмендегі сауалнаманы... text")
    # 4. block_rsvp (now only contains custom-rsvp-form)
    
    # So we remove block_956 and block_936 from their current places in the DOM
    block_956.extract()
    block_936.extract()
    
    # And we insert them right before `block_rsvp`
    block_rsvp.insert_before(new_venue_block)
    block_rsvp.insert_before(block_956)
    block_rsvp.insert_before(block_936)
    
    # Let's save!
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print("Blocks successfully reordered!")
else:
    print("Some blocks or elements are missing:")
    print("block_956:", bool(block_956))
    print("block_936:", bool(block_936))
    print("block_rsvp:", bool(block_rsvp))
    print("hosts_info:", bool(hosts_info))
    print("venue_card:", bool(venue_card))
