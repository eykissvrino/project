# Stage 4 (GWA 도출) — 전수 결과 해설서

> **연구진 보고용** · 자동생성: `pipeline/stage_report.py s4` (DB: `pipeline.duckdb`)  
> 설계 근거: `stages/Stage4_GWA_도출_설계.md` · 산출 엑셀: `outputs/S4_GWA도출.xlsx`  
> 본 문서는 **실제 전수 GWA 도출 결과와 품질지표**를 해설한다(설계안=무엇을 어떻게, 본 문서=무엇이 나왔는지).

---

## 1. 한눈에 — 전수 결과

- **입력(Stage 3 IWA)**: 178개
- **GWA(일반 작업활동)**: **41개** — O*NET 41 GWA를 한국어로 채택(하이브리드 주 트랙)
- **IWA→GWA 매핑**: **178 / 178 (strict 1:1 nesting)** — 모든 IWA가 정확히 1개 GWA에 귀속
- **실제 사용된 GWA**: **33 / 41** (KSCO 직업구조가 닿는 일반활동 범위)
- **4대 영역 분포**: 작업 산출 90 · 타인과의 상호작용 43 · 정신 과정 34 · 정보 입력 11

## 2. 품질 지표 종합

| 지표 | 기준 | 결과 | 판정 |
|---|---|---|---|
| nesting 무결성(중복배정 IWA) | 0 | **0** | ✅ strict 1:1 |
| 고아 IWA(매핑 없음) | 0 | **0** | ✅ |
| GWA 명사형(라벨 형태) | 명사구 | **100%** | ✅ ONET형 명사 범주 |
| 임베딩 cosine 중앙값 | 참고(게이트 아님) | 0.575 | 참고 |
| weak 매핑(cosine<0.55) | 보고 | 61 | 추상수준상 정상(전문가 분류 정본) |

## 3. 도출 방법 — 무엇을 어떻게

- **(주) 하이브리드 = O*NET이 실제로 한 방식**: GWA는 데이터에서 자생하는 군집이 아니라 **전문가가 설계한 Content Model 분류체계**(PAQ·직무분석 이론)다. 그래서 ONET 41 GWA를 **상위 어휘로 채택**(Opus 4.8 한국어 번역, 명사형 범주)하고, 각 IWA를 가장 맞는 GWA에 **매핑**했다.
- **매핑 = 임베딩(후보 생성) + Opus zero-shot(정본 분류) 2중**: GWA는 추상 수준이 높아 임베딩 최근접의 변별력이 낮다(상위 후보 간 cosine 격차 중앙값 0.017 — 178개 중 임베딩만으로 확실 분리는 19개뿐). 따라서 **41개 잘 정의된 범주 안에서 IWA의 본질(어느 영역·어떤 일반활동)을 보고 Opus가 1개를 zero-shot 분류**(ONET이 전문가 판단으로 한 것과 동형). 임베딩 cosine은 정합성 참고지표로 병기.
- **무-API**: 번역·분류 모두 구독 Opus 4.8 서브에이전트(외부 API/GPT 미사용).

## 4. 도출된 GWA — 규모 상위(소속 IWA 기준)

| GWA(한국어) | 영역 | O*NET 원문 | 소속 IWA |
|---|---|---|---|
| 물체 취급 및 이동 | 작업 산출 | Handling and Moving Objects | 50 |
| 기계 및 공정 제어 | 작업 산출 | Controlling Machines and Processes | 18 |
| 창의적 사고 | 정신 과정 | Thinking Creatively | 10 |
| 타인의 업무 및 활동 조정 | 타인과의 상호작용 | Coordinating the Work and Activities of Others | 9 |
| 대중 응대 및 직접 서비스 | 타인과의 상호작용 | Performing for or Working Directly with the Public | 9 |
| 타인 지원 및 돌봄 | 타인과의 상호작용 | Assisting and Caring for Others | 7 |
| 데이터·정보 분석 | 정신 과정 | Analyzing Data or Information | 6 |
| 기준 부합 여부 평가 | 정신 과정 | Evaluating Information to Determine Compliance with Standards | 5 |
| 일반 신체 활동 수행 | 작업 산출 | Performing General Physical Activities | 5 |
| 타인 훈련 및 교육 | 타인과의 상호작용 | Training and Teaching Others | 5 |
| 의사결정 및 문제해결 | 정신 과정 | Making Decisions and Solving Problems | 5 |
| 정보 입수 | 정보 입력 | Getting Information | 4 |
| 기계 장비 수리 및 정비 | 작업 산출 | Repairing and Maintaining Mechanical Equipment | 4 |
| 차량·기계 장치·장비 운전 | 작업 산출 | Operating Vehicles, Mechanized Devices, or Equipment | 4 |
| 판매 및 타인 설득 | 타인과의 상호작용 | Selling or Influencing Others | 3 |

## 5. 탐색 트랙(순수 상향식) — 가설 검증

"KSCO 데이터만으로 GWA를 상향식 도출하면 O*NET 41과 유사한가?"를 *반증 가능하게* 측정했다(같은 응집트리 최상위 절단).

- **자연 절단(k=3)**: 한국형 GWA가 **2개 거대군집만 자생** → O*NET 41 중 1개와만 매칭(평균 cos 0.5689).
- **ONET 수준(k=41 강제)**: 31개 군집 → 41 중 14개 매칭(평균 cos 0.5842).
- **결론**: 순수 상향식은 O*NET 41을 재현하지 못한다(자생 군집 ~2개). 이는 결함이 아니라 **GWA가 데이터 자생 구조가 아닌 전문가 설계 분류체계**임을 실증하며, 본 연구가 (주)하이브리드를 택한 근거다. 자생 거대군집과 ONET 비교는 `상향식탐색` 시트에 수록(자생 한국형 GWA 2개).

## 6. 정직한 한계
- **영역 쏠림**: 4대 영역 중 '작업 산출'에 90개 IWA가 몰린다. 이는 KSCO가 생산·기능·조작 직업(대분류 7·8·9)을 폭넓게 포괄한 직업구조의 반영이며, O*NET에서도 'Handling and Moving Objects'가 최대 GWA 중 하나인 것과 정합한다.
- **미사용 GWA 8개**: ONET 41 중 한국 IWA가 닿지 않은 일반활동(주로 세부 정보입력·특수 정신과정). 데이터 부재가 아니라 IWA 입도에서 해당 활동이 별도 분리되지 않은 결과.
- **임베딩 cosine의 의미**: 본 단계 cosine은 *배정 근거가 아니라* 정합성 참고치다(정본은 전문가형 Opus 분류). GWA 추상 수준에서 cosine 0.5~0.6대는 자연스럽다.

---

> **Stage 0~4 직무활동체계(TASK→DWA→IWA→GWA) 전수 구축 완료.** 다음(축2): 직업별 GWA 측정·프레임워크 범위(시범 중분류) — `stages/Stage5_*` 참조.
