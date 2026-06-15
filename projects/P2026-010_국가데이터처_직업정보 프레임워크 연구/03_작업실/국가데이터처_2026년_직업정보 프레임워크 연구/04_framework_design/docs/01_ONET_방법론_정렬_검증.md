# ONET WA 2014 방법론 정렬 검증서

> 본 설계 `00_프레임워크_종합설계서_v1.md`(v1.1)와 ONET Work Activities Project Technical Report (Hansen et al., 2014) 의 **1:1 정합·변형·기각 결정 추적표**.
> 작성: 이석주 · 2026-05-29
> 위치: `04_framework_design/docs/01_ONET_방법론_정렬_검증.md`

---

## 0. 본 검증서의 목적

본 연구의 NLP 파이프라인이 "ONET 방법론을 따랐다"고 주장할 때 — **어디는 그대로 차용, 어디는 한국 맥락으로 변형, 어디는 기각**했는지를 한 장에 추적 가능하게 만든다. 학회 발표 Q&A, 통계청 점검회의, 외부 자문 시 즉답용 근거 문서.

---

## 1. ONET 보고서 절차 항목 vs v1.1 반영 매핑

| # | ONET WA 2014 절차 | ONET 본문 위치 | v1.1 반영 절 | 차용·변형·기각 | 변형/기각 근거 |
|---|---|---|---|---|---|
| 1 | 귀납적 bottom-up 접근 (task → DWA → IWA → GWA) | §II General Methodology | §0·§2·§4 | **차용** | 한국 KSCO에도 동일 입자도 존재 |
| 2 | Quantitative(언어 분해) 접근 검토 후 기각 | §II p.13 | §5.5 | **기각의 기각** | LLM 의미 이해 능력이 2014 대비 질적 도약. 단, 인간 게이트는 유지 |
| 3 | Qualitative human judgment 채택 | §II p.13 | §5.5 | **부분 차용** | LLM이 qualitative 판단을 흉내내고, 위반·저신뢰 항목만 전문가 검수 |
| 4 | Task Clustering 3-step (Job Family → GWA → within-GWA) | §III pp.15–24 | §4.3 Step 3a/3b/3c | **차용** | 그대로. KECO 24를 Job Family 후보로 선정 |
| 5 | 22 SOC Major Group을 Job Family로 사용 | §III Table 3 | §4.3 Step 3a, §8 ① | **변형** | KECO 24 권장, KSCO 중분류 57은 차순위. 선택은 사용자 결정 |
| 6 | 41 GWA 버킷에 task 1:1 할당 (primary activity만) | §III Step 2 pp.17–19 | §4.3 Step 3b | **차용** | ONET 41 GWA를 그대로 사용 (한국 신규는 §4.4d에서 격리) |
| 7 | 3–4인 분석가 독립 할당 → consensus / majority rule | §III pp.18–19 | §4.3 Step 3b, §5.5 | **변형** | LLM 2-회 독립 실행 + self-consistency. 모델 다양성(Claude·GPT)으로 인간 다양성 대체 |
| 8 | GWA 내 7단계 정밀 클러스터링 | §III Step 3 pp.20–24 | §4.3 Step 3c | **변형(압축)** | 임베딩(bge-m3) + HDBSCAN으로 압축. 군집은 **GWA 버킷 단위**로 실행 |
| 9 | DWA Writing Standards 8조항 | §III p.24–25 + Appendix B | §4.3 Step 3c "8조항", §9 신규 산출물 `13_*` | **차용** | 한국어판으로 변환 후 LLM 라벨링 프롬프트에 강제 |
| 10 | DWA QC 4기준 (homogeneity / fit / specificity / uniqueness) | §III p.25 | §4.3 Step 3d | **차용** | 자동 검사 항목으로 추가 |
| 11 | Round-Robin 2회 QC (1차 QC팀 → 2차 QC팀) | §III p.26 | §4.3 Step 3d, §3 `qc_log` | **변형** | LLM 모델 2종 교차 검증으로 대체 + 위반 항목만 위원 검토 |
| 12 | Cross-Job-Family DWA 통합 | §IV p.26–27 | §4.4 Step 4a, 산출물 ⓕ | **차용** | 산업 간 직업 전환 가능성 분석의 직접 활용 |
| 13 | Multiple Linkage (task당 최대 3 DWA, 동일 Job Family 내) | §IV pp.27–28 | §4.4 Step 4b, §3 `task_to_dwa.link_order` | **차용** | 규약 그대로. 2-pass 분석은 LLM self-consistency로 대체 |
| 14 | Legacy DWA Integration (561 → 51 → 최종 10개) | §IV pp.28–29 | (한국 변형) | **변형** | 한국엔 legacy DWA가 없음. **대안**: 워크피디아·KNOW·NCS 활동 라벨을 "legacy 후보"로 두고 새 DWA와 비교하여 빠진 활동 흡수 |
| 15 | IWA Development: DWA를 다시 군집화하여 IWA 도출 | §V pp.29+ | §4.4 Step 4c | **차용** | **v1.0의 순서 오류 정정**. v1.1은 한국 IWA 신규 도출 후 ONET IWA와 비교 매핑 |
| 16 | DWA 채택 임계치: 최소 4 task 또는 3 직업 | §IV p.28 | §4.3 Step 3d | **차용** | 동일 |
| 17 | "Data–People–Things" 모델 기반 GWA 41 구조 | §III p.20 | §4.4 Step 4d | **차용** | ONET GWA 41 그대로 사용 |
| 18 | Online spreadsheet로 실시간 협업 | §III p.15 | §5.4 Streamlit 검토 웹 | **변형** | Streamlit으로 단일 직업 단위 협업 (동시 사용 ≤10명 가정) |
| 19 | Task type 구분 (Core vs Supplemental) | §III p.20 footnote | (반영 보류) | **부분 보류** | HumRRO 임계치(relevance ≥67% Core / 10–66% Supplementary)는 §4.2에 반영. KSCO 텍스트만으로는 core/supp 직접 라벨 어려움 — 시범적용 단계에서 시도 |
| 20 | 8th grade 가독성 목표 | §III p.25 | §4.3 "8조항 6번" | **차용 (한국어판 변환)** | 한국 중학교 2학년 가독성 |

---

## 2. 보고서·발표 Q&A 대비 5문항

**Q1. ONET이 quantitative 접근을 기각했는데 본 연구가 NLP·LLM 자동화를 채택한 것은 ONET 정신을 거스르는 것 아닌가?**

A. ONET 2014가 기각한 것은 "**단어 분해 + 통계적 분류**"이지 자동화 일반이 아니다. 본 연구는 LLM이 문장 전체를 의미적으로 이해(2014 NLP 대비 질적 도약)하므로 ONET이 우려한 "task statement 구조 다양성"을 다룰 수 있다. 단, **LLM 출력에 대한 인간 게이트는 유지** — 위반·저신뢰 항목은 전문가 검토 강제. 즉 ONET의 "human judgment 최후 보루" 원칙은 그대로다. 작업량을 1/10으로 축소하는 것일 뿐 검증 책임은 유지된다.

**Q2. 한국에서 22 SOC Job Family에 대응하는 것은 무엇인가?**

A. 두 후보 — KSCO 중분류 57 (통계 표준) vs KECO 24 (텍스트 친화). 본 설계는 **KECO 24를 권장**한다. 이유: (1) ONET 22와 입자도가 가깝다(직업당 task 수가 균형), (2) KECO는 KSCO 8차와 세분류 단위 1:1로 연결되어 통계 손실 없이 매핑 가능, (3) KSCO 중분류 57은 일부 중분류가 너무 거대(예: 23 사무직)하거나 너무 작아 within-family 클러스터링이 불균등. 단 최종 결정은 사용자에게 위임(§8 ①).

**Q3. Round-Robin 2회 QC를 LLM 모델 2종으로 대체한다는데, 이건 인간 다양성을 진짜 대체하는가?**

A. 완전 대체는 아니다. 모델 다양성(Claude·GPT)은 **문체·표현 편향 차이**를 잡지만 **문화적·산업적 맥락 편향**은 잡지 못한다. 그래서 본 설계는 모델 2종 불일치 항목 + DWA QC 4기준 위반 항목 + R점수 ≥2 직업을 **전문가 검토 큐로 강제 회부**한다(§4.3 Step 3d, §5.5). 즉 LLM은 1차·2차 QC를 자동화하고, 인간은 3차 QC로 격상되어 의심 항목에 집중한다. 인간 작업량은 줄고 결정 권한은 유지.

**Q4. Legacy DWA Integration이 한국에서 가능한가?**

A. ONET이 정의한 "legacy"(이전 DWA 2,164개)는 한국에 없다. 하지만 **기능적 대응물**은 있다 — 워크피디아·KNOW·NCS·한국직업사전의 활동 라벨. 본 설계는 이 활동 라벨들을 "legacy 후보"로 두고 새 한국 DWA와 비교하여 **누락된 활동이 있는지 외부 타당도 검증**한다(시범적용 단계, M+5). ONET 본문이 한 것과 같은 절차(561 후보 → 51 → 10 최종 채택)를 한국 데이터로 반복.

**Q5. ONET이 한 작업을 8개월에 압축한다는 게 가능한가?**

A. ONET 2014 프로젝트는 인간 분석가 3–4팀이 약 2년에 걸쳐 19,450 task를 처리했다. 본 연구는 KSCO 직업 495개(O*NET 974의 절반)에 한정되고, LLM이 1·2차 QC를 자동화하므로 명목상 4–6배 가속이 가능하다. **단 위험은 §6.4** — 전문가 검토 병목, LLM 비용, 8차 분리신설 31건 영향. 이에 대한 대응책을 사전 정의했다(우선순위 큐, 가중치, 재실행 트리거).

---

## 3. 보고서 본문 인용 예시

본 검증서의 표 1을 보고서 Ⅳ장(프레임워크 설계) 또는 부록에 그대로 삽입할 것을 권장. 예시 문장:

> 본 연구의 직무활동 4계층 도출 절차는 O\*NET Work Activities Project Technical Report (Hansen et al., 2014)의 Task Clustering 3-step 및 DWA Writing Standards 8조항을 1:1 차용하되, 8개월 사업기간 제약을 고려하여 인간 분석가의 GWA 할당 합의를 **대형 언어모델 2종(Claude·GPT)의 자기일치성 검사**로, Round-Robin 2회 품질관리를 **모델 교차 검증 + 전문가 검토 큐**로 대체하였다. 자세한 정합·변형 추적은 부록 [ONET 방법론 정렬 검증서]를 참조.

---

## 4. 다음 작업

- `13_DWA_Writing_Standards_8조항_한국어판.md` 작성 — 8조항 각각에 한국어 직업 사례 3건 (Good/Bad) 부착
- 시범적용 보고서에 본 표 1을 **검증 체크리스트**로 재사용 (각 항목 "준수/일부/미준수" 셀프 평가)

---

*v1.0 — ONET 본문 직접 인용 페이지 번호 명시. 발표 Q&A 즉답용.*
