const BOT_TOKEN = '8640737932:AAHsLpRu-PD3epqcA3-tqI8YaRaoSrba720';
const CHAT_ID = '1077964079';

async function testTelegram() {
  console.log('Testing Telegram connectivity...');
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    
    const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: CHAT_ID, text: 'Test from Node.js - сайт жұмыс істейді!' }),
      signal: controller.signal
    });
    clearTimeout(timeout);
    const data = await res.json();
    console.log('Response:', JSON.stringify(data));
  } catch (err) {
    console.error('ERROR:', err.message);
    if (err.name === 'AbortError') {
      console.log('\nКОНТЕКСТ: api.telegram.org-ға қосылу мүмкін болмады (timeout).');
      console.log('Бұл Қазақстандағы желі блокировкасынан болуы мүмкін.');
    }
  }
}

testTelegram();
