// Shared Claude API caller for all Vercel API routes

async function callClaude(system, userMsg, imgB64 = null, imgMime = 'image/jpeg', maxTokens = 1200) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return null;

  const content = [];
  if (imgB64) {
    content.push({ type: 'image', source: { type: 'base64', media_type: imgMime, data: imgB64 } });
  }
  content.push({ type: 'text', text: userMsg });

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: maxTokens,
      system,
      messages: [{ role: 'user', content }]
    })
  });

  if (!res.ok) {
    const err = await res.text();
    console.error('Claude API error:', res.status, err);
    return null;
  }
  const data = await res.json();
  return data.content?.map(b => b.text || '').join('') || null;
}

module.exports = { callClaude };