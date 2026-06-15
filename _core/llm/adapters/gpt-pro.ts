type Config = {
  apiKey?: string;
  model?: string;
  temperature?: number;
};

export class GPTProAdapter {
  private config: Config;
  private fetchFn: typeof fetch;
  constructor(config: Config) {
    this.config = config || {};
    // resolve fetch implementation (node-fetch for older Node)
    this.fetchFn = (typeof fetch === 'function') ? fetch : (async (...args: any[]) => {
      const fb = await import('node-fetch');
      return fb.default(...args);
    });
  }

  async chat(messages: Array<{ role: string; content: string }>, _options?: any): Promise<string> {
    const apiKey = this.config.apiKey || (typeof process !== 'undefined' ? process.env.OPENAI_API_KEY : undefined);
    if (!apiKey) throw new Error('OpenAI API key not configured (OPENAI_API_KEY)');
    const model = this.config.model || 'gpt-4';
    const body = {
      model,
      messages: messages.map(m => ({ role: m.role, content: m.content })),
      temperature: this.config.temperature ?? 0.7,
    };
    const res = await this.fetchFn('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    const message = data?.choices?.[0]?.message?.content ?? '';
    return message;
  }
}
