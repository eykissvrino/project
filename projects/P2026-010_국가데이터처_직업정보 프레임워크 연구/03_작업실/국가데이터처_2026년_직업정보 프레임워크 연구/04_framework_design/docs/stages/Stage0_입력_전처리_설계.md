# Stage 0 설계 — 입력 · 전처리 (KSCO 원천 → 추출가능 입력)

> 단계별 설계 시리즈 #0 · **v1.0 확정(2026-06-01, 쟁점 1~3 결정 반영)**
> 템플릿: ①목표 ②도출이론 ③입출력 ④방법 ⑤모델 ⑥소스코드 ⑦검증 ⑧쟁점
> 원칙: **본 단계는 "깨끗하고 단위가 확정된 입력"까지만** 책임진다. 무엇이 TASK인지 판정은 Stage 1.

---

## ① 목표·정의
- **목표**: KSCO 원천(정의·주요업무·예시)을 받아, **도출 단위(세세분류)별로 정제·상속·메타부착된 "추출가능 입력 레코드"**를 만든다.
- **추출가능 입력 레코드(extraction-ready record)** = 한 세세분류에 대해 {자기 정의, 자기 예시, 부모 세분류 정의·주요업무(상속), 메타(layer·source·plag)}가 정리된 1건.

## ② 도출 이론 (왜 이렇게)
- **GIGO 원칙**: 추출·군집 품질은 입력 품질의 상한을 못 넘는다 → 전처리가 토대.
- **3-Layer 소스 우선순위**(doc02): L0 KSCO 해설서(권위 100%, 전직업) ▶ L1 한국직업사전(조건부 보강) ▶ L2 NCS(극단부족). 본 단계는 **L0를 기본 입력**으로 확정하고, L1/L2 승급 *조건만* 정의(실행은 후속).
- **도출 단위 = 세세분류 + 부모 상속(D0)**: 주요업무는 세분류(4자리)에만 존재(0/1,270) → 자식 세세분류에 부모 주요업무를 상속해야 TASK 재료 확보.
- **단일 진실원천(SSOT)**: 모든 입력은 `pipeline.duckdb`에서 결정론적으로 조회 → 재현성.

## ③ 입력 → 출력 스키마
**입력(DuckDB, 적재 완료)**
| 테이블 | 핵심 필드 | 규모 |
|---|---|---|
| `ksco_occupation` | ksco_code, name, definition_text, main_tasks_text, examples_text, parent_code | 1,765 |
| `main_tasks_items` / `job_examples` | 정규화된 항목 | 2,367 / 7,622 |
| `mapping_ksco_keco` | KSCO↔KECO 중분류 | 495 |

**출력(추출가능 입력 레코드 — 메모리 dict 또는 뷰)**
```
{ ksco_code(5자리), name, parent_code(4자리), parent_name,
  definition_text(정제), examples_text, parent_definition_text, parent_main_tasks_text(정제),
  layer="L0", source="KSCO_HS", source_subject=null,
  low_signal: bool,           # 정의 빈약(이름·영문만)
  has_parent_tasks: bool,     # 부모 주요업무 존재
  valid: bool,                # 추출 가능 여부(자기 정의 또는 부모 주요업무 유효)
  remarks: str }              # 비고 — 예: "부모 주요업무 없음·자기정의 기반"(쟁점1 결정)
```

## ④ 도출 방법 (절차)
1. **단위 확정**: 세세분류(length=5) 1,270을 도출 단위로 열거. 부모=앞 4자리.
2. **상속 결합**: 부모 세분류의 정의·주요업무를 자식에 연결.
3. **텍스트 정제**:
   - 페이지헤더 노이즈 제거: `대분류 N`, `NNN┃한국표준직업분류`, 정의 앞 5자리 코드헤더.
   - 공백·줄바꿈 정규화(중복 공백 1개, 개행 제거).
   - (선택) 동의어 lexicon 치환.
4. **메타·플래그 부착**: layer/source/source_subject; `low_signal`(정의<50자 또는 ASCII비율>0.45); `has_parent_tasks`; `valid`(= 부모 주요업무 또는 자기 정의가 유효).
5. **추출 후보 분리**(경계 주의): 주요업무 글머리(·) 단위로 *후보 진술* 분리까지만. **행동진술 여부 판정은 Stage 1**.
6. **Layer 승급 조건 정의(실행은 후속)**: task<8 / 주요업무 없음 / 정의<80자 / R자기일치<0.7 / 군집미배치≥30% → L1 보강 대상 표시.

## ⑤ 사용 모델
- 대부분 **규칙 기반 전처리**(정규식). LLM 불요.
- (선택) Mecab-ko 형태소·Kss 문장분할 — *도구·환경 정규화나 동의어 처리에 한해*. 본 단계 핵심엔 불필요(현 Windows 환경 미설치, Sprint 3로 분리).

## ⑥ 소스코드 설계
| 파일 | 함수 | 상태 |
|---|---|---|
| `utils/ksco_fetch.py` | `fetch_for_extraction(con, code)`, `is_low_signal()`, `parent_code_of()`, `iter_scope()` | **구현됨** (상속조회·플래그·scope) |
| `utils/preprocess.py` (신규) | `clean_text(s)`(노이즈 제거), `normalize_ws(s)`, `build_record(con, code)`(메타·valid 종합), `coverage_report(con, scope)` | **신규 설계** |
| `parsers/ksco_handbook_parser.py` | 원천 적재 | 적재 완료 |
- `build_record`는 `fetch_for_extraction`를 감싸 정제·플래그까지 일괄. 출력 = ③ 스키마.
- 정제 결과는 **on-the-fly**(저장 안 함) 권장 — 재현성은 코드+DB로 보장.

## ⑦ 품질·검증 기준
| 지표 | 기준 | 현재(중분류28 표본) |
|---|---|---|
| 추출가능 커버리지 | 세세분류 중 valid 비율 | 48/51 (94%) — 전수 측정 필요 |
| 노이즈 잔존 | "대분류"·페이지헤더 0건 | (검증 루틴 필요) |
| low_signal 탐지 | name+EN 케이스 정탐 | 28433·22231 등 정탐 확인 |
| 단위 일관성 | 출력 1건 = 세세분류 1개 | OK |
- **검증 산출**: `coverage_report`가 전수 커버리지·무효직업 목록(직업사전 보강 대상)을 표로 출력.

## ⑧ 핵심 설계 결정 (확정)
1. **주요업무 없는 세분류 ~106개의 자식**: → **자기 정의로만 추출**하고, `remarks`(비고)에 "부모 주요업무 없음·자기정의 기반" 표기. L1 직업사전 보강은 *하지 않음*(표시만). 자기 정의도 빈약하면 `low_signal=true`로 같이 표시.
2. **직업명·소제목 필터 책임 경계**: → **Stage 1이 행동진술("~다" 종결·동사+목적어) 판정** 담당. Stage 0은 글머리 후보 분리 + 페이지노이즈 제거까지만.
3. **도구·환경**: → **TASK와 동시 추출(Stage 1)**. Stage 0에서 분리하지 않음.
4. **정제 결과 저장**: on-the-fly(코드+DB로 재현, 중간테이블 없음).

---

## 확정 (v1.0)
- 쟁점 1~3 결정 반영 완료. Stage 0 설계 **확정**.
- 다음: **Stage 1(TASK 도출) 설계**로 진행.
