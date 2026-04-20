import bs4
import re

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. Remove tilda-audio-player-button
for btn in soup.find_all(class_=re.compile('tilda-audio-player|tilda-audio-player-button')):
    btn.decompose()
    
# Or it might be a div wrapper
for div in soup.find_all('div', class_=re.compile('tilda-audio-player')):
    div.decompose()

# 2. Modify timer by stripping the seconds logic
timer_container = soup.find('div', id='countdown-timer')
if timer_container:
    # Find the block containing seconds
    sec_span = soup.find('span', id='seconds')
    if sec_span and sec_span.parent:
        sec_span.parent.decompose() # Remove the whole flex column for seconds

    # Also clean up the javascript snippet we injected
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'function updateTimer' in script.string:
            script_text = script.string
            # Remove the lines updating seconds
            script_text = re.sub(r'const seconds = Math.floor.*?;', '', script_text)
            script_text = re.sub(r"document.getElementById\('seconds'\).*?;", '', script_text)
            script.string.replace_with(script_text)

# Also do a raw string replace just in case
out_html = str(soup)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(out_html)

print("Removed custom audio player button and seconds from timer.")
