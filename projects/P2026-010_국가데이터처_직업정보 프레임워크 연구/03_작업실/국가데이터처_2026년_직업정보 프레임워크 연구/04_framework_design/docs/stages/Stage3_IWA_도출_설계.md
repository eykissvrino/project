# Stage 3 설계 — IWA(Intermediate Work Activities, 중간 작업활동) 도출

> 단계별 설계 시리즈 #3 · **v1.0 확정(2026-06-01)** — 절단A·cohesion 보고지표·ONET 명명 반영
> 입력: Stage 2의 DWA / 출력: IWA(중간 작업활동) + DWA↔IWA 연결
> 원칙(합의): 상향식 · 계층적 응집군집(같은 dendrogram 상위 절단) · 자연절단+ONET비율 · Opus 8조항 명명 · 두 트랙(하이브리드/순수) 공통

---

## ① 목표·정의
- **목표**: Stage 2의 DWA를 한 단계 더 일반화하여 **IWA(Intermediate Work Activity, 중간 작업활동)**를 도출하고 정식 명명.
- **IWA 정의**: 여러 DWA를 포괄하는 **중간 추상 수준** 작업활동. DWA(상세)와 GWA(일반) 사이.
  - 예: DWA "재무제표를 분석한다" + "투자 위험을 평가한다" + "신용도를 산정한다" → IWA "재무·투자 정보를 분석하여 판단한다".
- **위치**: GWA(41, 광범) ⊃ **IWA(중간)** ⊃ DWA(상세) ⊃ TASK. ONET: IWA 332개.

## ② 도출 이론 (왜)
- **ONET WA 3계층 구조**: ONET은 DWA(2,087)를 묶어 IWA(332)를 만들고 IWA를 GWA(41)에 연결. IWA는 **DWA와 GWA를 잇는 다리**.
- **단일 dendrogram 상위 절단**: Stage 2에서 만든 TASK 계층트리(또는 DWA medoid 트리)를 **더 높은 곳에서 절단** → IWA. 같은 트리라 **DWA ⊂ IWA nesting 자동 보장**(같은 DWA는 반드시 같은 IWA).
- **추상화 = 일반화**: DWA 진술들의 공통 본질을 한 단계 위 동사·목적어로 일반화(8조항, DWA보다 일반).
- **자연절단 + ONET 비율**: ONET DWA:IWA ≈ 6.3:1. 우리 DWA수 ÷ 6 근방을 broad band로 참고, 그 안에서 자연 plateau 절단.

## ③ 입력 → 출력 스키마
**입력**: Stage 2 `dwa`(라벨·medoid 임베딩·소속 TASK).
**출력**
```
iwa: {iwa_id, label(8조항), definition, n_dwa(소속 DWA수), n_task, n_jobs,
      mean_cosine, eight_rules_passed}
dwa_to_iwa: {dwa_id, iwa_id}      # 1:1 nesting (단일 트리)
```

## ④ 도출 방법 (절차)
1. **DWA 대표벡터**: 각 DWA의 medoid(또는 소속 TASK 임베딩 평균, 정규화) 산출.
2. **상향식 군집(IWA)**: 
   - **방법 A(권장·일관)**: Stage 2와 *같은* TASK dendrogram에서 **더 높은 높이로 절단** → IWA. DWA⊂IWA nesting 수학적 보장.
   - 방법 B(대안): DWA 대표벡터만 재군집(응집군집). 트리가 분리돼 nesting을 사후 매핑(DWA→다수결 IWA).
   → **방법 A 채택**(일관성·방어 우수).
3. **IWA 수준 절단(자연 + ONET band)**: DWA:IWA≈6:1 band 내 자연 plateau. 없으면 band 중앙(명시).
4. **IWA 명명(★ Opus, ONET 규약 = 동사구·일반)**: 각 IWA에 속한 DWA 라벨 5개를 Opus에 입력 → **목적어를 한 단계 일반화한 동사구**로 IWA 라벨 작성(DWA보다 일반, GWA보다 구체). 예: {재무제표를 분석한다, 투자위험을 평가한다, 신용도를 산정한다} → IWA **"재무·투자 정보를 분석하여 평가한다"**. 서브에이전트 배치.
5. **8조항 자동검증** → 위반 시 재작성(≤3).
6. **적재**: iwa / dwa_to_iwa(트랜잭션).

## ⑤ 사용 모델
- **군집**: scipy 계층군집(평균/Ward·코사인) — Stage 2와 동일 트리 상위 절단.
- **명명·재작성**: **Opus 4.8 단독**(구독·서브에이전트, API/GPT 없음).
- **8조항 검증**: 규칙.

## ⑥ 소스코드 설계
| 파일 | 함수/내용 | 상태 |
|---|---|---|
| `utils/clustering.py` | `cut_tree_at(Z, height)` 다층 절단(DWA·IWA·GWA 일관) | 보강 |
| `prompts/iwa_write_system.md` | IWA 8조항(DWA보다 일반) 명명 프롬프트 | **신규** |
| `utils/dwa_rules.py` | 8조항 검증(IWA 공용) | 공용 |
| `utils/iwa_build.py` | DWA→IWA 절단·명명·검증·persist | **신규** |
| `cli/kfw.py run cluster-iwa` | IWA 단계 가동 | 보강 |

## ⑦ 품질·검증 기준
| 지표 | 기준 |
|---|---|
| IWA 수 | DWA ÷ 5~8 (ONET 비율 band; ONET 6.3:1) |
| nesting 일관성 | 모든 DWA가 정확히 1 IWA에 속함(단일 트리) |
| IWA 응집도 | **보고 지표(게이트 아님)**. 참고치 ~0.55. ONET은 수치기준 없음(분석가 판단·트리 구조) → 절단수준은 자연절단+ONET비율로, cohesion은 품질 기술만. 전배정 유지 |
| 8조항 준수 | ≥ 0.90 |
| 추상도 검증 | IWA 라벨이 소속 DWA보다 일반적인지(전문가/육안 표본) |

## ⑧ 핵심 설계 결정 (확정)
1. **절단 방식 = A(같은 트리 상위절단)** — DWA⊂IWA strict nesting 수학 보장(ONET DWA→IWA 다중매핑 0건과 일치, 사후매핑 불필요).
2. **IWA 응집도 = 보고 지표(게이트 아님)**, 참고치 ~0.55. 절단수준은 자연절단+ONET비율(DWA:IWA≈6:1)로, cohesion은 품질 기술만(전배정 유지).
3. **IWA 명명 = ONET 규약(동사구·일반)**: Opus가 소속 DWA 라벨 5개 → 목적어를 한 단계 일반화한 동사구로 작성.
4. **빈 계층(IWA=DWA 수렴)**: DWA 적은 영역은 IWA가 DWA와 같아질 수 있음 — 허용(자연 결과).

## 확정 (v1.0)
- 절단 A · cohesion 보고지표 · ONET 동사구 명명 결정 완료. Stage 3 **확정**.
- 다음: **Stage 4(GWA 도출 — 하이브리드 채택 + 순수상향식 탐색) 설계**.
