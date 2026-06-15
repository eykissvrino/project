# HRM 컨설팅 AI 시스템

> HRM(임금·평가·성과·직무·조직) 전 영역 컨설팅을 위한 종합 AI 작업 환경

## 시스템 개요

본 시스템은 **HR 컨설팅 프로젝트의 전 수명주기를 AI로 지원**하기 위한 통합 작업 환경입니다.
Mercer/WTW, Korn Ferry/Hay, 한국형 자체 방법론을 상황별로 혼합 적용하며,
중소기업부터 대기업·공공·금융권까지 다양한 클라이언트에 대응합니다.

## 핵심 구성 요소

### 1. 전문 에이전트 (Agents)
| 에이전트 | 전문 영역 | 주요 활용 |
|----------|-----------|-----------|
| compensation-expert | 임금·보상 설계 | Pay Structure, Job Pricing, Pay Band 시뮬레이션 |
| performance-expert | 성과관리 | OKR/MBO, KPI 설계, 평가 캘리브레이션 |
| job-evaluation-expert | 직무평가 | IPE, Hay Method, JD, Job Matching |
| org-design-expert | 조직설계 | 조직구조, R&R, RACI, 권한위임 |
| hr-diagnostic-expert | HR 진단 | As-Is/To-Be, 갭 분석, 인터뷰 가이드 |
| labor-law-expert | 노동법 자문 | 통상임금, 취업규칙, 판례 검토 |
| consulting-writer | 문서 작성 | 제안서, 보고서, 매뉴얼 |
| research-analyst | 시장 조사 | 임금조사, 벤치마킹, 트렌드 분석 |

상세: `00_시스템/agents/`

### 2. HR 특화 스킬 (Skills)
| 스킬 | 사용 시점 |
|------|-----------|
| pay-structure-design | 임금체계 신규/재설계 시 |
| job-evaluation | 직무평가 수행 시 |
| salary-benchmarking | 시장 임금경쟁력 분석 시 |
| performance-system-design | 평가/성과제도 설계 시 |
| competency-modeling | 역량모델 개발 시 |
| org-design | 조직구조 설계 시 |
| hr-diagnostic | HR 전반 진단 시 |
| proposal-writing | 제안서 작성 시 |
| consulting-report | 컨설팅 보고서 작성 시 |
| hr-toolkit-build | 실무 엑셀모델/툴킷 제작 시 |
| change-management | 제도 도입 변화관리 시 |
| jd-development | JD 작성·표준화 시 |

상세: `00_시스템/skills/`

### 3. 지식베이스 (Knowledge Base)
- **방법론**: Mercer/WTW IPE, Hay Guide Chart, Korn Ferry, 한국형
- **법규 가이드**: 근로기준법, 통상임금 판례, 평가 관련 법규
- **시장정보**: 임금조사 레퍼런스, HR 트렌드
- **케이스 스터디**: 과거 프로젝트 인사이트

상세: `01_지식베이스/`

### 4. 템플릿 라이브러리
- 제안서 / 진단보고서 / 제도설계서 / 매뉴얼 / 엑셀모델

상세: `02_템플릿/`

## 사용 흐름

### 새 프로젝트 시작
```
"새 프로젝트 시작해줘. 클라이언트: ABC상사, 임금체계 진단"
→ 03_프로젝트/ABC상사_임금체계진단/ 폴더 자동 생성
→ Kickoff 템플릿 + 진단 워크플로우 자동 적용
```

### 특정 작업 요청
```
"직무평가 IPE로 진행하고 싶어"
→ job-evaluation-expert 에이전트 호출
→ job-evaluation 스킬 적용
→ Mercer IPE 방법론 적용
```

### 산출물 생성
```
"임금체계 진단보고서 초안 작성"
→ consulting-writer 에이전트 호출
→ consulting-report 스킬 적용
→ 02_템플릿/진단보고서/ 템플릿 기반 작성
```

## 폴더 구조

```
P2026-012_HRM_임금성과평가/
├── CLAUDE.md                    # AI 마스터 가이드
├── README.md                    # 본 문서
│
├── 00_시스템/                    # AI 시스템 코어 (수정 신중히)
│   ├── agents/                  # 전문 에이전트 정의
│   ├── skills/                  # HR 특화 스킬
│   └── workflows/               # 표준 컨설팅 워크플로우
│
├── 01_지식베이스/                 # 방법론·법규·시장정보·케이스
├── 02_템플릿/                    # 재사용 산출물 템플릿
├── 03_프로젝트/                  # 진행 중인 실제 프로젝트
└── 04_산출물_아카이브/            # 완료 산출물 보관
```

## 시스템 확장 원칙

1. **새 인사이트는 지식베이스에 축적** — 같은 케이스를 다시 풀지 말 것
2. **반복되는 산출 패턴은 템플릿화** — 매번 백지에서 시작하지 말 것
3. **새 방법론은 스킬로 모듈화** — 다른 프로젝트에서도 재사용 가능하게
4. **프로젝트 종료 시 산출물 + 학습 내용 아카이브** — 04_산출물_아카이브/ 활용

---

**버전**: v1.0 (2026-05-13)
**컨설턴트**: 이석주
