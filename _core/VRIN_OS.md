# VRIN OS — 마스터 개요 (최종 설계 v2.1)

> **이 문서가 VRIN AI 체계의 정문이다.** 전체를 한 장으로 보고, 5개 기둥으로 들어간다.
> **상태**: 설계 확정 · **개정**: 2026-06-15 · **소유**: 이석주 대표

---

## 0. 한 문장

> **"이석주 대표는 창업자다. AI는 매트릭스 조직(7부서) · 살아있는 위키 · 프로젝트를 거칠수록 똑똑해지는 회사다."**

---

## 1. 5대 원칙 + 행동강령

**원칙**: ① 나는 창업자, AI는 내 회사 ② 역할로 사고 ③ 멀티모델(Claude 메인+Codex+Antigravity) ④ 절차가 결과를 만든다(7단계) ⑤ 회사의 뇌는 공유된다
**행동강령**(Karpathy): ① 착수 전 사고 ② 단순함 우선 ③ 외과적 변경 ④ 목표 주도

---

## 2. 5개 기둥

| 기둥 | 문서 | 한 줄 |
|------|------|-------|
| 🏢 조직 | [`VRIN_ORG_SYSTEM.md`] | 매트릭스 — 7부서 × 프로젝트 스쿼드 + 거버넌스(@CoS·@BAR·@CLO) |
| 📁 프로젝트 | [`VRIN_PROJECT_STANDARD.md`] | `projects/` 표준 폴더 + 스쿼드 + 3-티어 승격 |
| 🧠 지식 | [`VRIN_SECOND_BRAIN.md`] | Second Brain(서랍) + LLM Wiki(살아있는 백과사전) |
| 📊 대시보드 | [`VRIN_COCKPIT.md`] | 로컬 HTML Cockpit — 프로젝트·스쿼드·부서가동률 실시간 |
| ♻️ 진화 | [`SYSTEM_EVOLUTION_LOOP.md`] | 매산출물→주→월→분기 자기진화 |

빌드: [`VRIN_BUILD_PLAN.md`]

---

## 3. 조직 한눈에 (매트릭스)

```
이석주 대표 → @CoS(PMO·라우팅·차출배분)   | 거버넌스: @BAR(품질) @CLO(진화)

기능부서(상시):  @STR전략 · @HR HR⭐ · @RES리서치 · @PT제품🚀 · @GTM그로스 · @DEL딜리버리 · @LEG법무
                    │ 각 부서 = 부서장 + 팀원(서브에이전트) 로스터
프로젝트(차출):  스쿼드 = 부서에서 차출한 cross-functional 팀 (리드 1 + 멤버 N)
```

## 4. 워크스페이스 한눈에

```
vrin_AI_hub/
├── _core/        AI 두뇌 (설계문서·부서/팀원 에이전트·스킬·표준)
├── _wiki/        🧠 회사 LLM 위키 (index·log·schema·pages) — 살아있는 지식
├── projects/     활성 프로젝트 (2026-05_고객사_사업명) + _대시보드 + _완료/
├── areas/        지속 책임 영역 (시앤피경영·HR솔루션팀·MBA·월인가)
└── cockpit.html  📊 실시간 현황 대시보드 (생성물)
```

## 5. 일의 흐름 & 성장

```
7단계: Frame→Plan→Produce→Critique(@BAR)→Validate→Deliver(@DEL)→Learn(@CLO→위키)
성장(3대 자산): 프로젝트 로컬(.claude/·02_지식) →검증→ 글로벌(_core/·_wiki/)
                에이전트 · 스킬 · 위키지식 — 고정 아님, 프로젝트 거칠수록 복리로 축적
```

## 6. 빌드 상태

✅ 설계(Phase 0) — 5개 기둥 확정 / ⏳ 구축(Phase 1~4) — [`VRIN_BUILD_PLAN.md`]

**검증 출처(7)**: oh-my-openagent · gstack · Karpathy(행동강령·LLM Wiki) · Anthropic 공식 · 닥터가드너 Second Brain · OMC wiki 도구 · 이석주 대표 11년 실무
