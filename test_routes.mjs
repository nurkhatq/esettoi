async function test() {
  // First test a simple GET
  const r1 = await fetch('http://localhost:3000/api/rsvp');
  console.log('GET /api/rsvp status:', r1.status, r1.headers.get('content-type'));
  const text1 = await r1.text();
  console.log('Body (first 200):', text1.substring(0,200));
  console.log('---');
  
  const r2 = await fetch('http://localhost:3000/api/admin');
  console.log('GET /api/admin status:', r2.status, r2.headers.get('content-type'));
  const text2 = await r2.text();
  console.log('Body (first 200):', text2.substring(0,200));
}
test().catch(console.error);
