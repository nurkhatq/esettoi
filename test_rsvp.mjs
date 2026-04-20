async function testRSVP() {
  console.log('Testing RSVP API...');
  try {
    const res = await fetch('http://localhost:3000/api/rsvp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Тест Қонақ', status: 'Келемін', wishes: 'Ұзақ өмір!' })
    });
    const data = await res.json();
    console.log('Status:', res.status);
    console.log('Response:', JSON.stringify(data));
  } catch (err) {
    console.error('ERROR:', err.message);
  }
}

testRSVP();
