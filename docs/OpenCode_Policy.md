# OpenCode 정책: Claude vs GPT/ Gemini 멀티모델 운영

- OpenCode 경로에서는 Claude를 비활성화하고 GPT Pro + Gemini Pro 두 모델만 사용하도록 구성했습니다. Claude는 ClaudeCode에서만 사용합니다.
- 두 모델은 _core/llm/index.ts 기반의 멀티모델 래퍼를 통해 런타임에 선택 가능하며, 환경 변수 OPENCODE_MODE으로 OpenCode 모드를 활성화하면 Claude 공급자에 대한 호출이 차단됩니다.
- 같은 폴더를 공유하더라도 충돌 없이 동작하도록 하위 계층에 경로 격리를 적용했습니다. Claude 관련 파일은 ClaudeCode용 폴더로 남겨 두고, OpenCode 경로는 GPT Pro 및 Gemini Pro 어댑터만 참조합니다.
- 운영 가이드는 필요 시 롤백 플랜과 모니터링 체크리스트를 포함해 점진적으로 업데이트합니다.

- 실행 가이드:
  1) OpenCode 모드 활성화: export OPENCODE_MODE=true
  2) GPT Pro, Gemini Pro를 위한 API 키 설정: OPENAI_API_KEY, GEMINI_API_KEY 환경 변수 설정
  3) 멀티모델 테스트: _core/llm/examples/multi-model-test.ts 예제 참고

참고: 이 문서는 코드베이스의 멀티모델 도입 전략과 운영 정책 변경을 돕기 위한 가이드이며, 변경사항은 PR로 기록해 주세요.
