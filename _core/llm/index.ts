// OpenCode-mode guard: Claude must be disabled in OpenCode projects
function __validateOpenCodeMode(provider: string) {
  const isOpenCodeMode = (process.env.OPENCODE_MODE || 'false').toLowerCase() === 'true';
  if (isOpenCodeMode && provider === 'claude') {
    throw new Error("Claude provider is disabled in OpenCode mode. Use 'gpt-pro' or 'gemini-pro' instead.");
  }
}

import { GPTProAdapter } from './adapters/gpt-pro';
import { GeminiProAdapter } from './adapters/gemini-pro';

export function createLLMClient(provider: string, config: any) {
  __validateOpenCodeMode(provider);
  if (provider === 'gpt-pro') return new GPTProAdapter(config);
  if (provider === 'gemini-pro') return new GeminiProAdapter(config);
  if (provider === 'claude') {
    // Claude is reserved for ClaudeCode; guard should block usage in OpenCode mode
    throw new Error("Claude provider is disabled in OpenCode mode. Use 'gpt-pro' or 'gemini-pro' instead.");
  }
  throw new Error('Unknown provider');
}
