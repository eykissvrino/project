type Config = {
  apiKey?: string;
  model?: string;
};

export class GeminiProAdapter {
  private config: Config;
  private fetchFn: typeof fetch;
  constructor(config: Config) {
    this.config = config || {};
    this.fetchFn = (typeof fetch === 'function') ? fetch : (async (...args: any[]) => {
      const fb = await import('node-fetch');
      return fb.default(...args);
    });
  }

  async chat(messages: Array<{ role: string; content: string }>, _options?: any): Promise<string> {
    const apiKey = this.config.apiKey || (typeof process !== 'undefined' ? process.env.GEMINI_API_KEY : undefined);
    if (!apiKey) throw new Error('Gemini API key not configured (GEMINI_API_KEY)');
    const model = this.config.model || 'gemini-3-pro';
    // This uses Gemini REST endpoint with a typical generateContent-like payload
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(apiKey)}`;
    const body = {
      contents: [{ parts: [{ text: messages.map(m => m.content).join('\n') }] }],
      // Optional: temperature/max tokens can be added if supported by endpoint
    };
    const res = await this.fetchFn(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    // Normalize: try to extract content from either 'choices' or 'payload'
    const text = data?.choices?.[0]?.message?.content ?? data?.content ?? '';
    return text;
  }
}
