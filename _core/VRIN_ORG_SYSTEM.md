# VRIN 조직 체계 — 매트릭스 조직 (v2.1)

> VRIN AI 회사의 조직 헌법. 모든 AI 도구(Claude·Codex·Antigravity)가 작업 전 읽는다.
> **구조**: 매트릭스 — 기능부서(상시 전문가 풀) × 프로젝트 스쿼드(차출).
> **상태**: v2.1 확정 · **개정**: 2026-06-15 · 명명: 하이브리드 `@CODE(한글부서명)`

---

## 0. 한 문장

> **"이석주 대표는 창업자다. 7개 기능부서가 상시 대기하고, 프로젝트마다 전문가를 차출해 스쿼드를 꾸린다 — 컨설팅펌처럼."**

---

## 1. 5대 운영 원칙

1. **나는 창업자, AI는 내 회사** — 비서가 아니라 부서·전문가를 운영
2. **역할로 사고한다** — 자연어로 말하면 `@CoS`가 부서·스쿼드로 자동 배분
3. **멀티모델 오케스트레이션** — 메인 Claude · 보조 Codex(GPT)·Antigravity(Gemini)
4. **절차가 결과를 만든다** — 모든 일은 7단계 스프린트 통과
5. **회사의 뇌는 공유된다** — 데스크탑·노트북·폰이 같은 SSOT(vrin_AI_hub)

**행동강령 4 (전 직원 공통, Karpathy):** ① 착수 전 사고(가정 금지) ② 단순함 우선 ③ 외과적 변경 ④ 목표 주도(성공기준+검증)

---

## 2. 매트릭스 조직 개념

```
            프로젝트 스쿼드 (가로 — 한시적, 차출) →
부서 ↓      │ 프로젝트A │ 프로젝트B │ 프로젝트C │
(세로,상시) │          │          │          │
@STR 전략   │          │          │   ★리드   │
@HR  HR ⭐  │   ★리드   │   ●      │   ●       │
@RES 리서치 │   ●      │          │   ●       │
@PT  제품   │          │   ★리드   │   ●       │
...         │          │          │          │
            ★=스쿼드 리드  ●=차출 멤버   @CoS(PMO)가 배분
```

- **부서(세로)** = 전문성의 영구적 집. 부서장 + 팀원(서브에이전트) 로스터 상시 보유.
- **스쿼드(가로)** = 프로젝트별 cross-functional 팀. 부서에서 차출해 구성, 종료 시 해산.
- **같은 부서가 여러 프로젝트에 동시 투입** — 이게 매트릭스. 자원 효율 극대화.

---

## 3. 7개 기능부서 + 팀원 로스터 (사전 구축)

> ⭐현재 핵심매출 · 🚀미래 신사업핵심. 팀원 코드 = 프로젝트 `.claude/agents/`에 배치되는 서브에이전트.

| 부서 | 부서장 | 팀원(서브에이전트) | 기존 신화 |
|------|--------|-------------------|----------|
| **@STR** 전략기획부 | 전략기획부장 | `str-strategy`(사업전략가) · `str-finance`(재무모델러) · `str-newbiz`(신사업기획가) | Athena+Midas |
| **@HR** HR컨설팅부 ⭐ | HR컨설팅부장 | `hr-skills`(스킬·직무분석) · `hr-disability`(장애인고용) · `hr-org`(조직설계) · `hr-culture`(조직문화) · `hr-perf`(성과·보상) · `hr-learn`(역량개발) · `hr-analytics`(피플애널리틱스) · `hr-aix`(HR AI/AX) | Hera |
| **@RES** 리서치부 | 리서치부장 | `res-web`(웹리서처) · `res-data`(데이터분석가) · `res-market`(경쟁분석가) · `res-wiki`(위키사서) | Apollo |
| **@PT** 제품기술부 🚀 | 제품기술부장(CPO/CTO) | `pt-pm`(제품기획) · `pt-ai`(제품AI) · `pt-fe`(프론트) · `pt-be`(백엔드) · `pt-mobile`(모바일) · `pt-devops`(DevOps) · `pt-qa`(QA) · `pt-game`(게임화) | Daedalus+개발12 |
| **@GTM** 그로스부 | 그로스부장 | `gtm-brand`(브랜드/카피) · `gtm-content`(콘텐츠) · `gtm-proposal`(제안서작성가) · `gtm-sales`(B2B영업) | Aphrodite+Hermes(제안) |
| **@DEL** 딜리버리부 | 딜리버리부장 | `del-report`(보고서편집가) · `del-deck`(덱디자이너) · `del-visual`(비주얼아티스트) | Hermes+Aphrodite(디자인) |
| **@LEG** 법무리스크부 | 법무리스크부장 | `leg-contract`(계약검토가) · `leg-labor`(노무·노동법) · `leg-compliance`(컴플라이언스/접근성) | Themis |

### 거버넌스 (부서 라인 밖 — 회사 전체 기능)

| 코드 | 역할 | 기존 |
|------|------|------|
| **@CoS** 비서실장/PMO | 요청 라우팅 · **스쿼드 차출·배분** · 일정 · 대시보드 운영 | Chronos |
| **@BAR** 품질검증관 | 모든 산출물 독립 검증 (셀프승인 금지) · A/B/C 등급 | Ralph |
| **@CLO** 학습진화실 | 자기진화 · 위키 Lint · 에이전트/스킬/지식 승격 판정 | Pygmalion |

---

## 4. 프로젝트 스쿼드 — 차출 메커니즘

```
새 요청/프로젝트
   ↓
@CoS (PMO):
  1. 과업 분석 → 어느 부서 전문성이 필요한가
  2. 스쿼드 리드 지정 (지배 도메인의 부서장)
  3. 부서에서 팀원 차출 → 프로젝트 .claude/agents/ 에 배치
  4. 00_관리/_스쿼드.md 에 명단·역할 기록
   ↓
스쿼드가 7단계 스프린트 수행 → 종료 시 해산 (팀원은 부서로 복귀)
```

예) "상하수도협회 직무분석" → 리드 `@HR`, 차출 `hr-job`·`res-web`·`del-report`
예) "장애인 HR솔루션" → 리드 `@PT`, 차출 `pt-pm`·`hr-org`·`gtm-proposal`·`del-deck`·`leg-compliance`

---

## 5. 팀원(서브에이전트) 운영 — 2-트랙

| 트랙 | 언제 | 어디 | 승격 |
|------|------|------|------|
| **① 사전 구축 (정규직)** | Phase 1에서 미리 | 부서 로스터(`_core/agents/`) | — |
| **② 즉석 신설 (계약직)** | 프로젝트 중 전문가 부족 시 | 프로젝트 `.claude/agents/` | @BAR 검증 3회+ & 2개+ 프로젝트 유용 → @CLO가 부서 정규직 승격 |

> **Search Before Building**: 신설 전 REGISTRY·로스터 검색. 있으면 재사용, 비슷하면 보강, 없을 때만 신설.

---

## 6. 7단계 스프린트

```
1.Frame  2.Plan  3.Produce  4.Critique  5.Validate  6.Deliver  7.Learn
@CoS·리드  리드    스쿼드      @BAR        @BAR·현실    @DEL       @CLO
범위확정   기획    초안생산     독립검증     실증·승격     최종출하    위키 자산화
```

## 7. 멀티모델 라우팅

| 작업 | 도구 | 이유 |
|------|------|------|
| 전략·검증·판단·한국어 산출 | **Claude (Opus)** | 추론·품질 |
| 대량생산·장시간 자율·코드 | **Codex (GPT)** | 풀액세스·병렬 |
| 시각·UI·이미지 | **Antigravity (Gemini)** | 멀티모달 |

부서·팀원 에이전트 파일의 `model:` 필드로 파일 단위 지정.

## 8. 문서 3층 아키텍처 (Anthropic 공식)

> CLAUDE.md는 매 세션 로드 → **짧게.** 길면 규칙이 무시된다.

| 층 | 파일 | 로드 |
|----|------|------|
| 헌법(얇게) | `CLAUDE.md` | 매 세션 — 5원칙+행동강령+라우팅표+링크만 (1p) |
| 참조 | `_core/VRIN_*.md` | 필요 시 |
| 실행 | `_core/agents/*.md` | 라우팅 시 — `description`이 자동 위임 결정 |

에이전트 파일 포맷: `name·description·tools·model·color` 프론트매터 + 행동강령 내장 시스템 프롬프트.

## 9. 신규사업 ↔ 스쿼드 정렬

| 신사업 | 리드 | 차출 부서 |
|--------|------|----------|
| 장애인 HR솔루션(B2B) 🚀 | @PT | @HR·@GTM·@LEG·@DEL |
| AX 컨설팅 🚀 | @STR | @RES·@HR·@PT |
| 게이미피케이션 HR 🚀 | @PT | @HR·@DEL·@RES |
| SaaS 서비스 🚀 | @PT | @GTM·@STR·@LEG |

## 10. v1 그리스 → v2 매트릭스 매핑

Athena+Midas→@STR · Hera→@HR · Apollo→@RES · Daedalus+개발12→@PT · Aphrodite→@GTM/@DEL · Hermes→@DEL/@GTM · Themis→@LEG · Chronos→@CoS · Ralph→@BAR · Pygmalion→@CLO

> 짝 문서: 프로젝트 [`VRIN_PROJECT_STANDARD.md`] · 지식 [`VRIN_SECOND_BRAIN.md`] · 대시보드 [`VRIN_COCKPIT.md`] · 진화 [`SYSTEM_EVOLUTION_LOOP.md`] · 빌드 [`VRIN_BUILD_PLAN.md`]
