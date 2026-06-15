# Stage 4 설계 — GWA(Generalized Work Activities, 일반화 작업활동) 도출

> 단계별 설계 시리즈 #4 · **v1.0 확정(2026-06-08)** — 2중매핑·한국신규허용·자연절단+ONET비교·4영역 반영
> 입력: Stage 3의 IWA / 출력: GWA + IWA↔GWA 연결
> 합의: **(주) 하이브리드 = ONET 41 한국어 채택 → IWA를 매핑** · **(탐색) 순수 상향식 = KSCO만으로 GWA 도출 → ONET 일치도 비교**

---

## ① 목표·정의
- **목표**: IWA를 최상위로 일반화하여 **GWA(일반화 작업활동)**를 확정. 두 트랙 동시:
  - **(주) 하이브리드**: ONET 41 GWA(한국어)를 **상위 어휘로 채택**, 각 IWA를 가장 맞는 GWA에 **매핑** → 정보분석/정신과정/업무수행 등 **ONET 형태 보장**.
  - **(탐색) 순수 상향식**: 같은 dendrogram 최상위 절단으로 **한국형 GWA 자생 도출** → ONET과 **몇 % 일치하는가** 비교(가설 검증·학술 기여).
- **GWA 정의**: 직업·산업 무관 **가장 일반적인 작업활동 범주**. ONET: 41개(4영역). 형태는 **명사형**("정보 입수", "데이터·정보 분석").

## ② 도출 이론 (왜)
- **ONET 사실**: GWA는 데이터 군집이 아니라 **전문가 설계 Content Model 분류체계**(PAQ·직무분석 이론). 그래서 순수 상향식으로 41 재현은 어렵다(우리 실측 자연군집 ~5).
- **하이브리드 = ONET이 실제로 한 방식**: GWA top-down 선재 + DWA/IWA를 거기에 매핑. → ONET 형태 GWA를 얻는 정석.
- **순수 상향식 = 가설 검증**: "KSCO만으로 GWA를 도출하면 ONET과 유사한가"를 *반증 가능하게* 측정 → 결과가 발산해도 "한국 직업구조 고유성"으로 연구 정보.
- **구성타당도**: 한국형 체계 ↔ ONET 수렴 정도로 타당성 보고.

## ③ 입력 → 출력 스키마
**입력**: Stage 3 `iwa`(라벨·대표벡터).
**출력**
```
gwa: {gwa_id, label_kr, onet_gwa_id(ONET 41 코드), onet_label_en,
      is_kr_unique(한국 신규 여부), source('ONET_adopt'|'KR_bottomup')}
iwa_to_gwa: {iwa_id, gwa_id, cosine(IWA↔GWA 유사도), method('mapped'|'clustered')}
# (탐색 트랙) gwa_bottomup: {kr_gwa_id, label_kr, n_iwa, nearest_onet, cosine}
```

## ④ 도출 방법 (절차)

### 트랙 1 — 하이브리드(주)
1. **ONET 41 GWA 한국어화**: ONET 41 GWA 라벨·정의를 Opus로 **1회 일괄 번역**(캐시) → `gwa.label_kr`. (정보 입수, 데이터·정보 분석, 의사결정 및 문제해결 …)
2. **IWA → GWA 매핑**: 각 IWA 대표벡터 ↔ ONET 41 GWA(한국어 라벨+정의) 임베딩 **최근접**. cosine 기록.
   - 보강: 임계 미만(애매)은 Opus가 IWA 진술 보고 41 중 택1(zero-shot) — 임베딩+LLM 2중.
3. **한국 신규 GWA 격리**: 최근접 cosine < 0.55 이고 의미상 ONET 41에 없으면 `is_kr_unique=true`(한국 특이활동). (ONET 보고서 신규 격리 절차 차용)
4. **적재**: gwa / iwa_to_gwa.

### 트랙 2 — 순수 상향식(탐색)
5. **최상위 절단**: Stage 2의 *같은 dendrogram*을 더 높이 절단 → 한국형 GWA 자생 도출(자연절단; 개수 강제 없음).
6. **ONET 비교**: 한국형 GWA 중심벡터 ↔ ONET 41 최근접 → **일치 GWA 수 / 평균 유사도** 산출.
7. **보고**: "KSCO 자생 GWA n개, ONET 41 중 m개와 매칭(평균 cos)" → 가설 검증 결과(정직).

## ⑤ 사용 모델
- **번역·zero-shot 매핑·신규 판정**: **Opus 4.8 단독**(구독, API/GPT 없음).
- **임베딩 매핑**: bge-m3.
- **상향식 절단**: scipy 계층군집(같은 트리).

## ⑥ 소스코드 설계
| 파일 | 함수/내용 | 상태 |
|---|---|---|
| `parsers/onet_gwa_translate.py` | ONET 41 GWA 한국어 번역(Opus 1회·캐시) → gwa.label_kr | **신규** |
| `prompts/gwa_map_system.md` | IWA→GWA zero-shot 매핑(41 in-context) | **신규** |
| `utils/gwa_build.py` | (트랙1) 매핑·신규격리 / (트랙2) 상향식 절단·ONET비교 | **신규** |
| `utils/clustering.py` | `cut_tree_at` 최상위 절단(Stage 2 트리 재사용) | 공용 |
| `cli/kfw.py run map-iwa-gwa` | GWA 단계 가동 | 보강 |

## ⑦ 품질·검증 기준
| 지표 | 기준 |
|---|---|
| (주) IWA→GWA 매핑 신뢰 | 임베딩+LLM 일치율 ≥ 0.80, 애매건 Opus 재판정 |
| 한국 신규 GWA | cosine<0.55 격리, 비율 보고(과다 시 매핑 점검) |
| (탐색) ONET 일치 | 한국 GWA ↔ ONET 매칭 수·평균 cos 보고(가설) |
| GWA 명사형 | 라벨이 ONET형 명사구인지(번역 품질) |
| nesting | 모든 IWA가 정확히 1 GWA(주 트랙) |

## ⑧ 핵심 설계 결정 (확정)
1. **하이브리드 매핑 = 임베딩 최근접 + 애매건 Opus zero-shot 2중**. 토큰 부담 작음(ONET 번역 1회 + 애매 IWA 수십 회). 구독(Claude MAX)이라 요금 0.
2. **한국 신규 GWA = 허용**(cos<0.55 격리, `is_kr_unique`). 한국 고유 GWA가 도출되면 더 가치 — 단 실증 분석 후 확정.
3. **탐색 트랙 = 자연절단 그대로 분석 + ONET 비교**(개수 강제 없음). ONET 41 수준 절단도 참고 병기.
4. **GWA 4대 영역 표기 = 채택**(정보입력·정신과정·작업산출·타인과상호작용) — 보고 가독성.

> 핵심 재확인: **KSCO 직업설명 → TASK → DWA → IWA → GWA** 구축. ONET은 (주)GWA 어휘 채택 + (탐색)비교 기준으로만 사용.

## 확정 (v1.0)
- Stage 4 결정 완료. → **Stage 0~4 전체 설계 완료.**
- 다음(선택): 전체 설계 통합 검토 / 구현 착수(시범 중분류 검증).
