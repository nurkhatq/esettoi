import bs4

html_path = 'd:/toi/esettoi/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# 1. REMOVE "әуен" (case insensitive)
for node in soup.find_all(string=True):
    # Skip script and style blocks
    if node.parent.name in ['script', 'style']:
        continue
    text = node.get_text()
    if text and 'әуен' in text.lower():
        # User requested to remove texts like "әуен қосы" or "әуен қосу"
        # We will empty the string entirely or clear its parent if it's just this text.
        node.replace_with('')

# 2. FIX THE COUNTDOWN TIMER
# To do this safely, we will find "Қалған уақыт", and inject a custom countdown script right there.
timer_title = soup.find(string=lambda t: t and 'Қалған уақыт' in t)
if timer_title:
    # Look for the timer block that has the numbers 00
    # Let's find the parent container holding the timer
    timer_block = timer_title.parent
    for _ in range(3):
        if timer_block and timer_block.name == 'div' and ('r' in timer_block.get('class', []) or 't-rec' in timer_block.get('class', [])):
            break
        if timer_block and timer_block.parent:
            timer_block = timer_block.parent
    
    # We will inject a custom JS script and a fresh HTML struct into timer_block to handle countdown correctly.
    # First, let's clear the static "00" or just inject our own dynamic timer and hide the rest.
    custom_timer_html = """
    <div id="custom-timer-container" style="text-align:center; padding: 40px 10px;">
        <h2 style="font-family: 'KZAstanaPro-Medium', serif; color: #AD9A6B; margin-bottom: 20px;">Күнтізбе</h2>
        <div style="font-family: inherit; font-size: 20px; color: #333; margin-bottom: 30px;">
            13 Маусым 2026, Сағат 18:00
        </div>
        <div style="font-family: 'KZAstanaPro-Medium', serif; color: #AD9A6B; margin-bottom: 15px; font-size: 24px;">Қалған уақыт</div>
        <div id="countdown-timer" style="display: flex; justify-content: center; gap: 15px; font-family: sans-serif; opacity: 0; transition: opacity 0.5s;">
            <div style="display:flex; flex-direction:column; align-items:center;">
                <span id="days" style="font-size: 32px; font-weight: bold; color: #333; background: rgba(173,154,107,0.1); padding: 15px; border-radius: 8px; min-width: 60px;">00</span>
                <span style="font-size: 14px; margin-top: 5px; color: #666;">күн</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center;">
                <span id="hours" style="font-size: 32px; font-weight: bold; color: #333; background: rgba(173,154,107,0.1); padding: 15px; border-radius: 8px; min-width: 60px;">00</span>
                <span style="font-size: 14px; margin-top: 5px; color: #666;">сағат</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center;">
                <span id="minutes" style="font-size: 32px; font-weight: bold; color: #333; background: rgba(173,154,107,0.1); padding: 15px; border-radius: 8px; min-width: 60px;">00</span>
                <span style="font-size: 14px; margin-top: 5px; color: #666;">мин</span>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center;">
                <span id="seconds" style="font-size: 32px; font-weight: bold; color: #AD9A6B; background: rgba(173,154,107,0.1); padding: 15px; border-radius: 8px; min-width: 60px;">00</span>
                <span style="font-size: 14px; margin-top: 5px; color: #AD9A6B;">сек</span>
            </div>
        </div>

        <script>
            function updateTimer() {
                // Event Date: June 13, 2026, 18:00
                const eventDate = new Date("2026-06-13T18:00:00").getTime();
                const now = new Date().getTime();
                const distance = eventDate - now;

                if (distance < 0) {
                    document.getElementById('countdown-timer').style.opacity = 1;
                    return;
                }

                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);

                document.getElementById('days').innerText = days < 10 ? '0'+days : days;
                document.getElementById('hours').innerText = hours < 10 ? '0'+hours : hours;
                document.getElementById('minutes').innerText = minutes < 10 ? '0'+minutes : minutes;
                document.getElementById('seconds').innerText = seconds < 10 ? '0'+seconds : seconds;
                
                document.getElementById('countdown-timer').style.opacity = 1;
            }
            setInterval(updateTimer, 1000);
            updateTimer();
        </script>
    </div>
    """
    
    # We clear out the old block to destroy the broken static countdown and bad text formatting like "00күн00сағат", then put our modern clean counter.
    if timer_block:
        # Save a reference to it
        timer_block.clear()
        timer_block.append(bs4.BeautifulSoup(custom_timer_html, 'html.parser'))
        print("Replaced whole timer block with custom dynamic countdown")
        
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Finished updates.")
