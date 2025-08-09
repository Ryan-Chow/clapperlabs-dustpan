// Keep your API key in environment variables, never in code
const CLAUDE_API_KEY = 'key'; // Never hardcode this

const testClaudeAPI = async () => {
  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-3-5-haiku-20241022',
        max_tokens: 100,
        messages: [
          { role: 'user', content: 'Hello, this is a test.' }
        ]
      })
    });
    
    const data = await response.json();
    console.log('API Response:', data);
  } catch (error) {
    console.error('API Error:', error);
  }
};

testClaudeAPI();