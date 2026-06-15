# VRIN 리소스 레지스트리 (v2.1 — 매트릭스)

> 이석주 대표의 AI 회사에서 가용한 에이전트·스킬·프로젝트의 통합 카탈로그.
> **버전**: v2.1 매트릭스 · **갱신**: 2026-06-15 · 상위: [`VRIN_OS.md`](VRIN_OS.md)
> v1(그리스 신화) → v2(실리콘밸리 매트릭스) 전환 완료. v1 백업: `archive/agents-v1-greek-20260615/`

---

## 1. 조직 — 43 에이전트 (`_core/agents/v2/`)

### 거버넌스 (3)
| 코드 | 파일 | 역할 | model |
|------|------|------|-------|
| @CoS | cos.md | 비서실장/PMO — 라우팅·스쿼드 차출·대시보드 | opus |
| @BAR | bar.md | 품질검증관 — 독립검증·A/B/C (셀프승인 금지) | opus |
| @CLO | clo.md | 학습진화실 — 진화·위키 Lint·3대 자산 승격 | opus |

### 기능부서 7 + 팀원 (40)

| 부서 | 부서장 | 팀원(서브에이전트) |
|------|--------|-------------------|
| **@STR** 전략기획 | str | str-strategy · str-finance · str-newbiz |
| **@HR** HR컨설팅 ⭐ | hr | hr-skills · hr-disability · hr-org · hr-culture · hr-perf · hr-learn · hr-analytics · hr-aix |
| **@RES** 리서치 | res | res-web · res-market · res-data · res-wiki |
| **@PT** 제품기술 🚀 | pt | pt-pm · pt-ai · pt-fe · pt-be · pt-mobile · pt-devops · pt-qa · pt-game |
| **@GTM** 그로스 | gtm | gtm-proposal · gtm-brand · gtm-content · gtm-sales |
| **@DEL** 딜리버리 | del | del-report · del-deck · del-visual |
| **@LEG** 법무리스크 | leg | leg-contract · leg-labor · leg-compliance |

> 매트릭스: 부서(세로,상시) × 프로젝트 스쿼드(가로,차출). 부서장=opus(Task로 팀원 호출), 팀원=sonnet.
> 모든 에이전트에 행동강령 4 내장. 상세 [`VRIN_ORG_SYSTEM.md`](VRIN_ORG_SYSTEM.md).

---

## 2. 자동 라우팅 (자연어 → 부서)
직무·조직·인사·교육·장애인고용→@HR / 전략·신사업·재무→@STR / 조사·데이터·위키→@RES / 웹·앱·제품·게임화→@PT / 마케팅·제안서·영업→@GTM / 보고서·덱·비주얼→@DEL / 계약·노무·접근성→@LEG / 현황·일정·새프로젝트→@CoS

---

## 3. 스킬 (Tier 2, `_core/skills/`)
컨설팅·문서 26종 (consulting-report·job-analysis·proposal·hr-consulting·org-diagnosis·strategic-management·business-planning·legal-consulting·branding-marketing·project-management·pptx·docx·pdf·mermaid 등). 부서별 활용은 각 에이전트 파일 참조.
> `project-management`는 P2026-003·P2026-010 프로젝트 패턴을 일반화해 승격(2026-06-16). 도메인 특화 진행관리는 프로젝트 로컬 유지.
> 신규 스킬은 프로젝트 `.claude/skills/`에 신설 → 검증 → @CLO가 글로벌 승격 ([`VRIN_PROJECT_STANDARD.md`](VRIN_PROJECT_STANDARD.md) §5).

## 4. 지식 — LLM Wiki (`_wiki/`, Phase 3 구축 예정)
회사 지식자산. Ingest/Query/Lint by @RES(res-wiki)·@CLO. [`VRIN_SECOND_BRAIN.md`](VRIN_SECOND_BRAIN.md).

## 5. 프로젝트 (`projects/`)
명명 `{연도}-{번호}_{고객사}_{사업명}`. 현황은 `00_관리/_현황.md` → `cockpit.html`. [`VRIN_PROJECT_STANDARD.md`](VRIN_PROJECT_STANDARD.md).
> 기존 15개(P2026 시리즈)는 점진 이관 — 작업 시 표준화.

## 6. 플러그인·MCP
mckinsey-pptx · oh-my-claudecode(wiki 도구 포함) / hwp-mcp · notion · figma

---

## 7. 관리 규칙
| 변경 | 갱신 대상 |
|------|----------|
| 에이전트 추가/제거 | REGISTRY · CLAUDE.md 라우팅표 |
| 스킬 추가 | REGISTRY · 프로젝트→글로벌 승격 시 @CLO |
| 프로젝트 생성/완료 | REGISTRY · _대시보드 |
| 진화 주기 | 매산출물(@BAR)→주→월→분기(@CLO) — [`SYSTEM_EVOLUTION_LOOP.md`](SYSTEM_EVOLUTION_LOOP.md) |
