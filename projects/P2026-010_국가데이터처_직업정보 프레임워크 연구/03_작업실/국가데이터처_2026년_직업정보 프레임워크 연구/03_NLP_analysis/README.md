# 03_NLP_analysis — NLP 5단계 핵심 파이프라인 (v1.4 실 가동 기준)

> 본 폴더는 본 연구의 **핵심 분석 엔진** 가동 공간이다.
> 전체 설계: `04_framework_design/docs/00_프레임워크_종합설계서_v1.md` (v1.4)
> 핵심 스킬: `.claude/skills/nlp-job-analyzer/`

---

## 폴더 구조 (v1.4)

```
03_NLP_analysis/
├── scripts/                              ← 코드
│   ├── requirements.txt                  ← Python 의존성
│   ├── .env.example                      ← LLM API 환경변수 템플릿
│   ├── cli/
│   │   └── kfw.py                        ← 단일 진입점 (typer CLI)
│   ├── parsers/                          ← 외부 데이터 파서
│   │   ├── ksco_handbook_parser.py       ← KSCO 8차 해설서 PDF → DB ✔
│   │   ├── keco_parser.py                ← KECO 2025 xlsx (TODO)
│   │   ├── kjd_parser.py                 ← 한국직업사전 PDF (TODO)
│   │   ├── onet_parser.py                ← ONET 18.0 (TODO)
│   │   └── isco_appendix4_parser.py      ← ISCO 평가연구 부록4 (TODO)
│   ├── prompts/                          ← LLM 프롬프트 텍스트 (Jinja)
│   │   ├── extract_tasks.j2              (M+1 작성)
│   │   ├── assign_gwa.j2                 (M+2 작성)
│   │   ├── label_dwa_8rules.j2           (M+2 작성)
│   │   └── score_responsibility.j2       (M+3 작성)
│   ├── utils/                            ← 공통 유틸 (전처리·LLM client·캐시)
│   └── web_streamlit/                    ← 검토 웹 (CBM intervention)
│       └── app.py                        (M+2 베타)
├── models/                               ← 임베딩·LLM 캐시
│   └── .gitkeep
└── results/
    ├── pipeline.duckdb                   ← 단일 저장소 (init 후 생성)
    ├── cache/                            ← LLM 호출 캐시
    └── snapshots/                        ← 단계별 Parquet 스냅샷
```

---

## 첫 가동 절차 (M+1)

```bash
cd 국가데이터처_2026년_직업정보\ 프레임워크\ 연구

# 1. Python 환경
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r 03_NLP_analysis/scripts/requirements.txt

# 2. 환경변수
cp 03_NLP_analysis/scripts/.env.example 03_NLP_analysis/scripts/.env
# 편집기로 .env 열어 API 키 입력

# 3. DuckDB 초기화 (19개 테이블 생성)
python 03_NLP_analysis/scripts/cli/kfw.py init

# 4. KSCO 8차 해설서 import (첫 import)
python 03_NLP_analysis/scripts/cli/kfw.py ingest ksco --version 8 \
  --source "01_data_collection/00_external_references/직업정보 관련 참고자료_국내/한국표준직업분류_2024년 고시_8차/(해설서) 제8차 한국표준직업분류(공개용)_24.6.24_(최종안) (1).pdf"

# 5. 파일럿 3중분류 전처리
python 03_NLP_analysis/scripts/cli/kfw.py run preprocess --layer L0 --scope 28,22,24
```

---

## 5단계 파이프라인 (재참조)

ONET WA 2014 보고서의 절차를 1:1 차용, 한국·LLM 맥락으로 변형. 상세 절차는
`04_framework_design/docs/01_ONET_방법론_정렬_검증.md` 표 1 참조.

| 단계 | CLI 명령 | 산출 |
|---|---|---|
| ① 전처리 | `kfw run preprocess` | processed parquet |
| ② TASK 추출 | `kfw run extract-tasks --runs 2` | `task` 테이블 |
| ③ DWA 도출 (3-pass) | `kfw run jf-split → gwa-bucket → cluster-dwa → dwa-qc` | `dwa` |
| ④ 정련 + IWA | `kfw run cross-family-dwa → multi-linkage → cluster-iwa-kr → map-iwa-gwa` | `iwa`, `gwa`, 매핑 |
| ⑤ Responsibility | `kfw run score-resp --runs 2` | `responsibility` |

---

## 산출물 위치

- 직무기술 정의서 1건: `kfw report definition --ksco <code> --format docx` → `06_deliverables/.../{ksco}.docx`
- 한국형 GWA/IWA/DWA 사전: `kfw report dictionary` → `06_deliverables/final_report/`
- 시뮬레이션 결과: `kfw eval all` → `05_simulation/results/`

---

## v1.4 변경

- 폴더 구조 표준화 (scripts/cli·parsers·prompts·utils·web_streamlit)
- typer CLI 단일 진입점 (`kfw.py`)
- DuckDB DDL 19개 테이블 + 4개 view + ONET schema
- LLM 최상위급 (Opus 4 + GPT-5) 환경변수 템플릿
- 첫 가동 절차 명문화
