# 시앤피 AI 스킬맵 v4.0 — 마스터 문서

## CnP AI Skill Map — Master Document (Systematically Derived)

**작성**: 2026-05-30 (토) | 이석주
**구성**: 본 문서(도출 체계·구조 총괄·문헌 매핑) + `CSF_v4.0_AI스킬맵_시각화.html` + `CSF_v4.0_AI스킬맵_스킬인벤토리.xlsx`
**v3.2 → v4.0 변경**: ①도출 체계 명시(매트릭스·선별기준·명명규칙) ②전문 명명(국·영문) ③스킬 카드 심화(세부 스킬 요소·산출물 추가) ④40스킬로 재구성
**상태**: 자문회의 1차(2026.6) SME 검증 예정 | 이전 버전(v2.x·v3.0~3.2) 전부 폐기

---

## 1. 도출 체계 — 어떻게 도출했는가

### 1.1 도출 매트릭스: 보편 업무 가치사슬 × AI 협업 모드

스킬은 임의 나열이 아니라 두 축의 교차에서 도출했다.

- **가로축 — 보편 업무 가치사슬** (모든 산업 공통): ①탐색·수집 → ②처리·분석 → ③생산·작성 → ④소통·실행 → ⑤운영·자동화
- **세로축 — AI 협업 모드**: M1 Assist(보조) → M2 Delegate(위임·자동화) → M3 Transform(재설계)

| 역량군 | 매트릭스 위치 | 도출 논리 |
|---|---|---|
| **F. AI 코어** | 전 단계 공통 인터페이스 | 지시·검증·보안은 모든 셀의 전제 조건 → 횡단 배치 |
| **A1. 리서치·지식** | ①탐색·수집 × M1·M2 | 검색·요약(M1) + 딥리서치·모니터링 위임(M2) |
| **A3. 데이터·의사결정** | ②처리·분석 × M1·M2 | 대화형 분석(M1) + 정제·예측 자동화(M2) |
| **A2. 콘텐츠·커뮤니케이션** | ③생산 + ④소통 × M1 | 문서·시각물·커뮤니케이션의 AI 공동 생산 |
| **A4. 자동화·에이전트** | ⑤운영·자동화 × M2 | 프로세스 자동화 + 에이전트 위임·오케스트레이션·감독 |
| **T. 트랜스포메이션** | 전 단계 × M3 | 가치사슬 자체를 재설계·확산 — ★시앤피 AX 시그니처 |

### 1.2 선별 기준 (4대 — 전 스킬 통과 검증)

1. **보편성** — 산업·직무 무관 적용 가능
2. **수요 근거** — 문헌·트렌드에서 빈도 입증 (글로벌 12프레임 + 국내 사례 + 2026 트렌드)
3. **측정 가능성** — 행동·산출물로 평정 가능 (BOS·BARS 작성 가능 여부로 검증)
4. **교육 가능성** — Skillset이 교육과정 1개로 전환 가능

### 1.3 명명 규칙

- 「업무 대상·맥락」+「AI 작업 유형」의 **전문 명사형** (예: "회의록 자동화·액션 도출")
- **국문+영문 병기** (글로벌 호환: Meeting Intelligence & Action Tracking)
- 금지: 범용 동사형(~하기), 유행 제품·모델명
- 세부 기법·도구는 **'세부 스킬 요소'와 '현재 표현형'**에 배치 (내구성 확보)

### 1.4 스킬 카드 표준 (8필드)

정의 / **세부 스킬 요소 4** / **산출물 예시 2** / 행동지표 BOS 3(빈도) / 숙련수준 BARS 5(L1인지~L5전파) / 현재 표현형(연 1회 갱신) / 근거 출처 / 소속 경로

---

## 2. 전체 구조 (6역량군 · 13역량 · 15Skillset · 40Skill)

```
〔Band T · 워크 트랜스포메이션〕★         T. AI 워크 트랜스포메이션 (2역량·6스킬)
  McKinsey: 재설계 기업 2.75배 성과         T1 워크플로우 리디자인 | T2 AX 확산·체인지 리딩
                  ▲
〔Band A · 실무 활용〕 25스킬               A1 AI 리서치·지식관리 (2역량·8스킬)
  업무활동 4영역 = 스킬의 본체              A2 AI 콘텐츠·커뮤니케이션 (2역량·6스킬)
                                           A3 AI 데이터 분석·의사결정 (2역량·6스킬)
                                           A4 AI 자동화·에이전트 (2역량·5스킬) ←2026 최대 갭
                  ▲
〔Band F · 코어〕 9스킬                     F. AI 코어 스킬 (3역량·9스킬)
  전 직원 공통 토대                         F1 프롬프트·컨텍스트 설계 | F2 산출물 검증·품질관리
                                           F3 리스크·컴플라이언스
```

### 2.1 40스킬 전체 목록 (국문 — 영문)

**F. AI 코어 스킬** (AI Core Skills)
| ID | 스킬 | 영문 |
|---|---|---|
| F01 | 과업 프롬프트 설계 | Task Prompt Design |
| F02 | 반복 개선·프롬프트 체이닝 | Iterative Refinement & Prompt Chaining |
| F03 | 컨텍스트·참조자료 구성 | Context & Reference Engineering |
| F04 | 프롬프트 템플릿·자산화 | Prompt Assetization & Standardization |
| F05 | 팩트체크·출처 검증 | Fact-Checking & Source Verification |
| F06 | 환각·오류 탐지 | Hallucination & Error Detection |
| F07 | 산출물 보정·품질 확정 | Output Refinement & Quality Finalization |
| F08 | AI 정보보안·프라이버시 관리 | AI Data Privacy & Security |
| F09 | AI 저작권·규제 준수 | AI Copyright & Regulatory Compliance |

**A1. AI 리서치·지식관리** (AI Research & Knowledge)
| ID | 스킬 | 영문 |
|---|---|---|
| A01 | AI 검색·질의 설계 | AI Search & Query Design |
| A02 | 딥리서치 위임·종합 | Deep Research Delegation & Synthesis |
| A03 | 동향 인텔리전스 운영 | Trend Intelligence Operations |
| A04 | 문서 요약·핵심추출 | Document Summarization & Key Extraction |
| A05 | 회의록 자동화·액션 도출 | Meeting Intelligence & Action Tracking |
| A06 | 다국어 번역·현지화 | AI Translation & Localization |
| A07 | 문서 기반 Q&A 구축 | Document-Grounded Q&A (RAG) |
| A08 | 지식베이스 구축·관리 | Knowledge Base Curation |

**A2. AI 콘텐츠·커뮤니케이션** (AI Content & Communication)
| ID | 스킬 | 영문 |
|---|---|---|
| A09 | 보고서·기획서 AI 작성 | AI-Assisted Report & Proposal Writing |
| A10 | 비즈니스 커뮤니케이션 작성 | Business Correspondence with AI |
| A11 | 교정·윤문·톤 최적화 | Editing & Tone Optimization |
| A12 | 프레젠테이션 설계·생성 | AI Presentation Design |
| A13 | 이미지 생성·편집 | AI Image Generation & Editing |
| A14 | 영상·오디오 생성 | AI Video & Audio Production |

**A3. AI 데이터 분석·의사결정** (AI Data & Decision)
| ID | 스킬 | 영문 |
|---|---|---|
| A15 | 데이터 정제·전처리 | AI Data Cleaning & Preparation |
| A16 | 스프레드시트 AI 활용 | AI-Powered Spreadsheet Operations |
| A17 | 대화형 데이터 분석 | Conversational Data Analytics |
| A18 | 시각화·대시보드 구축 | AI Visualization & Dashboarding |
| A19 | 예측·시뮬레이션 활용 | AI Forecasting & Scenario Simulation |
| A20 | 데이터 스토리텔링·보고 | Data Storytelling & Executive Reporting |

**A4. AI 자동화·에이전트** (AI Automation & Agents) — 2026 최대 스킬 갭 영역
| ID | 스킬 | 영문 |
|---|---|---|
| A21 | 업무 프로세스 자동화 | AI Process Automation |
| A22 | AI 코딩·업무도구 개발 | AI-Assisted Tooling & Citizen Development |
| A23 | 에이전트 과업 설계·위임 | Agent Task Design & Delegation |
| A24 | 멀티스텝 워크플로우 구축 | Multi-Step Agent Workflow Orchestration |
| A25 | 에이전트 모니터링·휴먼 오버사이트 | Agent Monitoring & Human Oversight |

**T. AI 워크 트랜스포메이션** (AI Work Transformation) ★
| ID | 스킬 | 영문 |
|---|---|---|
| T01 | AI 기회 진단·우선순위화 | AI Opportunity Assessment & Prioritization |
| T02 | 워크플로우 리디자인 | AI Workflow Redesign |
| T03 | 성과 측정·ROI 관리 | AI Impact Measurement & ROI |
| T04 | 베스트 프랙티스 확산 | Best Practice Scaling |
| T05 | AI 역량 코칭 | AI Capability Coaching |
| T06 | 팀 AI 운영체계 구축 | Team AI Operating Model |

> 각 스킬의 **정의·세부 스킬 요소·산출물·BOS·BARS·표현형·출처**는 Excel '스킬카드_BOS_BARS' 시트 또는 HTML 스킬 클릭으로 확인.

### 2.2 수준 체계 (전 스킬 공통, KIRD·IBM 정합)

| Lv | 명칭 | 정의 |
|---|---|---|
| L1 | 인지 | 알고 있으며 안내에 따라 시도한다 |
| L2 | 활용 | 정해진 업무에 독립적으로 정기 수행한다 |
| L3 | 적용 | 상황에 맞게 조정·판단하며 능숙하게 수행한다 |
| L4 | 통합 | 팀 업무 체계에 통합하고 타인을 지도한다 |
| L5 | 전파 | 새 방식·표준을 만들어 조직에 확산한다 |

---

## 3. 문헌 활용 매핑 (설계 요소 → 근거)

| 설계 요소 | 근거 문헌 |
|---|---|
| 3밴드 위계 (코어→실무→전환) | McKinsey 3-Layer · 삼성/LG/SK 교육 위계 · IBM Foundations→Mastery |
| 실무 4영역 | **시앤피 KTR 제안서 v5.0 4대 영역(원형)** · WEF New Economy Skills 계층 |
| 코어 밴드 (지시·검증·책임) | **Anthropic 4D** · Google AI Essentials · BCG critical thinking · EU AI Act Art.4 · 한국 AI기본법 |
| 트랜스포메이션 밴드 ★ | **McKinsey Rewiring(2.75배)** · Deloitte 2026(84% 미재설계) · AX Blender 4단계 · **시앤피 산인공 자산** |
| 에이전트 스킬 (A23~25) | Deloitte 2026(에이전틱 74% vs 거버넌스 21%) · **Workera 벤치마크(숙련 13%)** · 삼성SDS Agent 3단계 · 2026 오케스트레이션 시프트 |
| 스킬 중심·K/A 제외 | **김은경 외 2024** · 딜로이트 2026 HC(스킬 기반 조직) · NCS 2025 |
| BOS+BARS 이원 측정 | **KIRD 과학기술인 역량사전** (표1-1·표4-52~55) |
| 5수준 | KIRD 5수준 · IBM 5단계 |
| 기술 중립 명명·표현형 분리 | 2026 트렌드(프롬프트→컨텍스트→하니스) · SFIA 분리 원칙 |

전체 25건 서지·활용 상세: Excel '문헌출처' 시트 / HTML 하단.

---

## 4. 운용·다음 단계

**스킬 기반 HR 운용**: 진단(BOS 120 + BARS) → Job-Skill Profile 갭 분석 → Skillset 단위 교육 매칭(1 SS = 과정 1개) → PBL 인증 → 연 1회 인벤토리 개정(가변층만).

**KTR 적용 경로**: ①자문회의 1차 SME 검증 → ②친환경 바이오화학 직무군별 Job-Skill Profile(S3) → ③기존 25개 과정 × 40스킬 매핑(S4) → ④협약기업 수요조사에 BOS 진단지 활용(S5).

---

*v4.0: 2026-05-30 / 도출 매트릭스 기반 체계 도출. 6군·13역량·15SS·40스킬 / BOS 120·BARS 200 / 세부 스킬 요소 160·산출물 80 / 근거 25건.*
