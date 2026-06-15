# O*NET Prototype Project Final Report (1995) 분석

## 0. 문서 메타정보

| 항목 | 내용 |
|---|---|
| 제목 | Development of Prototype Occupational Information Network (O*NET) Content Model — Volume I: Report |
| 저자 | Norman G. Peterson, Michael D. Mumford, Walter C. Borman, P. Richard Jeanneret, Edwin A. Fleishman |
| 발주 | 미국 노동부(DOL) / 유타 주 노동력서비스부 (Contract No. 94-542) |
| 발행 | 1995년 9월 |
| 분량 | 695페이지 (Volume I 본문 + Volume II 부록 9종 설문지) |
| 위상 | 현행 O*NET 콘텐츠 모델의 원형 설계 문서. APDOT 권고를 구체화한 최초의 설계서 |

---

## 1. 문제의식: DOT의 한계와 O*NET의 등장 배경

미국 노동부 *Dictionary of Occupational Titles*(DOT, 1991년 4판)의 한계가 출발점이다.

- **과업 중심 기술의 한계**: 1만 개 직업을 직무분석가의 관찰·면담 기반 과업 기술로 작성 → 직업 간 비교 곤란, 일반화된 분류·집계 불가
- **사람 속성 정보의 부재**: Abilities, Knowledges, Skills, Interests 등 작업자 속성 누락
- **갱신 비용 과다**: 자료 노후화, 기술·산업 변화 추적 불가
- **타 DB와 연결성 부족**: 정성적 서술 형식이라 임금·산업·노동시장 자료와 결합 어려움

→ APDOT(Advisory Panel on the DOT, 1993)이 "다목적·공통어·확장 가능한 데이터베이스형 직업정보 시스템"을 권고했고, 이 보고서가 그 구현 모델인 **Content Model**을 제안한다.

---

## 2. O*NET Content Model의 6개 도메인 구조

| 도메인 | 하위 디스크립터 | 성격 |
|---|---|---|
| **Worker Characteristics** (작업자 특성) | Abilities / Occupational Values & Interests / Work Styles | 영속적·비가변적 인간 속성 |
| **Worker Requirements** (작업자 요건) | Basic Skills / Cross-Functional Skills / Knowledges / Education | 경험·교육으로 발달하는 역량 |
| **Experience Requirements** (경험 요건) | Training / Experience / Licensure | 직무 진입 전 누적 자격 |
| **Occupational Requirements** (직업 요건) | Generalized Work Activities (GWA) / Work Context / Organizational Context | 직업이 요구하는 활동·상황·조직 환경 |
| **Occupation-Specific Requirements** (직업 특수 요건) | Occupational Skills / Knowledges / Tasks / Duties / Machines, Tools, Equipment | 특정 직업 고유 정보 |
| **Occupation Characteristics** (직업 특성) | Labor Market Information / Occupational Outlook / Wages | 노동시장·경제 환경 |

### 모델 설계의 4가지 근본 원리

1. **사람 속성 vs. 직무 속성** 구분
2. **교차직업(cross-occupation) vs. 직업특수(occupation-specific)** 구분 — DOT에 없던 핵심 축
3. **가변적 요건 vs. 비가변적 특성** 구분
4. **위계적(hierarchical) 조직** — 사용자가 분석 목적에 따라 거시·미시 수준을 선택

이 위계 구조 덕분에 직업특수 정보(과업·도구)가 GWA·기술 등 상위 교차직업 디스크립터로 자연스럽게 묶이며, "공통어 + 확장성"을 동시에 확보한다.

---

## 3. 각 도메인의 디스크립터 (요약)

### Skills (Chapter 3)
6개 상위 군집으로 위계화:
- Basic Skills (읽기, 쓰기, 수리, 청취, 말하기, 학습 등)
- Complex Problem Solving Skills
- Social Skills
- Technical Skills
- Systems Skills
- Resource Management Skills

각 군집은 higher-order / lower-order로 다시 분류. SCANS 보고서, 인지심리·산업조직심리 문헌과의 정합성을 검증.

### Knowledges (Chapter 4)
교차직업 지식 분류 체계 — 후일 O*NET이 33개 지식 영역(Administration, Engineering, Mathematics, Customer Service 등)으로 정착되는 출발점.

### Abilities (Chapter 10)
**Fleishman의 Ability Requirements Approach** 기반 — Cognitive / Psychomotor / Physical / Sensory 4개 대범주를 위계적 인지능력 모델로 구성. 행동기준평정척도(BARS)로 측정.

### Generalized Work Activities (Chapter 6)
McCormick PAQ, Cunningham OAI의 인자분석 결과를 종합 — "기계·공정 통제", "정보 처리", "타인과의 상호작용" 등 직업 횡단적 작업활동 차원.

### Work Context (Chapter 7) / Organizational Context (Chapter 8)
물리적 환경뿐 아니라 사회적 맥락(대인관계·자율성·역할갈등)과 조직 맥락(산업·구조·문화·인사제도)까지 포함 — DOT에 없던 핵심 확장.

### Occupation-Specific (Chapter 14)
위계적 연역 절차로 직업특수 과업·기술을 도출. GWA로 과업 자극(prompt)을 만들어 SME 패널이 과업 진술을 신속·일관되게 생성 → 수집 비용·시간 대폭 절감.

---

## 4. 방법론적 핵심

### (1) Taxonomy 구축 3단계 (Fleishman & Mumford 1991)
1. 분석 단위(domain) 정의 → **"position"(개인 단위)** 채택
2. 디스크립터 집합 선정 → 이론·실증 연구 양쪽에서 추출
3. 구성 타당도 검증 → 내적·외적 타당도 양면

### (2) 측정 도구 — 9종 표준 설문 (Volume II 부록)
| 부록 | 설문 |
|---|---|
| A | Skills Questionnaire |
| B | Knowledges Questionnaire |
| C | Training, Education, Licensure, Experience |
| D | Generalized Work Activities |
| E | Work Context |
| F | Organizational Context |
| G | Abilities |
| H | Occupational Values |
| I | Work Styles |

기본 척도: **Level**(복잡성·요구수준) × **Importance**(중요도). 일부 변수는 취득 시기·장소 등 추가 척도 병행.

### (3) 응답자 전략
- 분석가 평정 우월성에 대한 실증 근거 부족 → **재직자(incumbent) 중심**
- 조직 맥락 등 가시성 낮은 변수는 관리자 별도 수집
- 6학년 가독성 수준으로 문항 설계 → 신규 직업 출현 감지 능력 확보

### (4) 비용 효율성
- 모든 직업에 동일 설문 적용 → 단일 도구로 다수 직업 기술
- CATI, 디스켓 우편, 인터넷 등 다중 채널 수집 권고

---

## 5. 한국 국가데이터처 직업정보 프레임워크 연구에 대한 시사점

### 직접 활용 가치가 높은 부분
1. **6도메인 구조** — KECO/KSCO와 별개로 "사람-직무-맥락-시장" 다축 설명 모델로 도입 가능
2. **위계적 분류 체계 설계 방법론** — 정책·교육·HR·연구 다목적 활용을 동시 만족시키는 구조
3. **교차직업 vs. 직업특수 디스크립터의 분리** — KSCO 직업 단위 분류와 별개로 cross-cutting 분류 축 추가의 근거
4. **재직자 중심·표준설문 기반 데이터 수집 모델** — 워크넷·고용정보원 데이터 수집 체계 재설계 참조
5. **GWA 기반 연역적 과업 도출 방법론** — 수만 개 직업 갱신 비용 문제 해결의 실증적 모델

### 참고 시 주의점
- 1995년 시점 모델 → 플랫폼 노동, AI 직무, 그린·돌봄 직무 등 신생 영역은 별도 보강 필요
- 미국 노동시장과 한국 표준직업분류·고용직업분류 매핑은 별도 과제
- O*NET 후속 개정(Content Model 6.0 등)에서 일부 디스크립터 변경 → **현행 O*NET 콘텐츠 모델과 병행 검토** 필수

---

## 6. 결론(Chapter 15) 핵심 메시지

- 단일 모델로 모든 사용자의 모든 질문에 답할 수 없으나, **위계적 구조**가 다양한 사용 수준을 동시 수용
- 콘텐츠 모델은 **확장 가능한(extensible) 설계** — 하위 수준에 변수를 추가해 특수 응용 대응
- 직업특수 정보 수집은 cross-occupation 분류 체계를 활용한 연역 방식이 효율적
- 시범적용(field test) 결과를 바탕으로 본격 O*NET 개발 단계로 진행할 것을 권고
