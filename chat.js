const { callClaude } = require('./_claude');
const { AGENT_PROMPTS } = require('./_knowledge');

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    return res.status(200).end();
  }
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  const { messages, llm = 'claude', _system_override, _img_b64, _img_mime } = req.body || {};
  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json({ error: 'messages array required' });
  }

  const system = _system_override || AGENT_PROMPTS.chatbot;
  const lastUserMsg = [...messages].reverse().find(m => m.role === 'user')?.content || '';
  let responseText = null;

  try {
    if (llm === 'gemini' && process.env.GEMINI_API_KEY) {
      const gRes = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: system + '\n\n' + lastUserMsg }] }]
          })
        }
      );
      if (gRes.ok) {
        const gData = await gRes.json();
        responseText = gData?.candidates?.[0]?.content?.parts?.[0]?.text || null;
      }
    } else if (llm === 'openai' && process.env.OPENAI_API_KEY) {
      const oRes = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
        body: JSON.stringify({
          model: 'gpt-4o-mini',
          max_tokens: 600,
          messages: [{ role: 'system', content: system }, ...messages.map(m => ({ role: m.role === 'assistant' ? 'assistant' : 'user', content: m.content }))]
        })
      });
      if (oRes.ok) {
        const oData = await oRes.json();
        responseText = oData?.choices?.[0]?.message?.content || null;
      }
    }

    // Default / fallback: Claude
    if (!responseText) {
      responseText = await callClaude(system, lastUserMsg, _img_b64 || null, _img_mime || 'image/jpeg', 600);
    }

    if (!responseText) {
      responseText = 'I am unable to connect to the AI service right now. Please try again shortly.';
    }

    return res.status(200).json({ response: responseText, llm_used: llm });
  } catch (err) {
    console.error('Chat error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
}