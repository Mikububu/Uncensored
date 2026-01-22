const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const OPENROUTER_API_KEY = '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';
    
    const requestBody = JSON.parse(event.body);
    
    console.log('🎨 Netlify Function forwarding to OpenRouter...');
    
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aprils-spielzeugkasten.netlify.app",
        "X-Title": "Uncensored Studio"
      },
      body: JSON.stringify({
        "model": "black-forest-labs/flux.2-pro",
        "messages": requestBody.messages || [{"role": "user", "content": requestBody.prompt || ""}],
        "modalities": ["image", "text"]
      })
    });

    const data = await response.json();
    
    console.log('✅ OpenRouter response status:', response.status);
    
    return {
      statusCode: response.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: JSON.stringify(data)
    };
    
  } catch (error) {
    console.error('❌ Netlify Function error:', error);
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ error: error.message })
    };
  }
};