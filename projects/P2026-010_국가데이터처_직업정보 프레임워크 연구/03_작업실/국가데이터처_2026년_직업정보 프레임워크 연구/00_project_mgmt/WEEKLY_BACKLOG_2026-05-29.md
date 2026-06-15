# 이번 주 백로그 — 2026-05-29 ~ 06-04

> 출처: `04_framework_design/docs/04_수행계획서_실무가동_v1.md` §8
> 목적: 매일 체크할 단위 작업 — 완료 시 [x] 표기, 이슈 시 비고

---

## Phase 0 사전작업 (착수)

- [ ] **0.1 KSCO 8차 해설서 PDF → Excel 5시트 추출**
  - 입력: `01_data_collection/00_external_references/직업정보 관련 참고자료_국내/한국표준직업분류_2024년 고시_8차/(해설서) 제8차 한국표준직업분류(공개용)_24.6.24_(최종안) (1).pdf` (1,036p)
  - 출력: `01_data_collection/processed/ksco_handbook_v8.xlsx`
  - 시트: 대분류 / 중분류 / 소분류 / 세분류(495) / 세세분류
  - 컬럼(세분류 시트): `ksco_code`, `ksco_name`, `정의`, `주요업무`, `세세분류_명단`, `8차_변동플래그`
  - 도구: Claude Code + pdfplumber
  - 예상 소요: 0.5일
  - DoD: 세분류 row count = 495, 정의·주요업무 null < 5%

- [ ] **0.2 KSCO 분류항목표 hwpx → Excel**
  - 입력: `01_data_collection/00_external_references/.../제8차+한국표준직업분류+개정+분류+항목표.hwpx`
  - 출력: `01_data_collection/processed/ksco_classification_v8.xlsx` (단일 시트)
  - 컬럼: `level`(대/중/소/세/세세), `code`, `name`, `parent_code`
  - 도구: Claude Code + zipfile (hwpx 내부 XML 직접 파싱)
  - 예상 소요: 0.5일
  - DoD: 4계층 모두 row 존재, parent_code 무결성

- [ ] **0.3 0.1·0.2 검수 리포트**
  - 출력: `01_data_collection/processed/_import_log.md`
  - 항목: 0.1 vs 0.2 코드 일치율, 누락·중복, OCR 의심 케이스
  - 도구: Claude Code + Pandas
  - 예상 소요: 0.5일
  - DoD: 누락 코드 0건, 의심 케이스 < 10건

- [ ] **0.4 DuckDB 초기화 + KSCO 적재 (kfw 1차 가동)**
  - 사전 조건: `03_NLP_analysis/scripts/cli/kfw.py`의 `init` · `ingest ksco` 명령 동작 확인
  - 작업: `python kfw.py init` → `python kfw.py ingest ksco --version 8 --source <0.1산출>`
  - 도구: Python CLI
  - 예상 소요: 1일 (parser 실구현 포함 시)
  - DoD: `SELECT COUNT(*) FROM ksco_occupation WHERE ksco_level='세분류'` = 495

- [ ] **0.5 KECO 2025 연계표 적재**
  - 입력: `한국고용직업분류 2025 개정 - 한국표준직업분류 8차 간 연계표_20250103043442.xlsx`
  - 출력: DuckDB `mapping_ksco_keco` 테이블
  - 도구: Pandas + DuckDB
  - 예상 소요: 0.5일
  - DoD: 양방향 매핑, KECO 중분류 수 실측값 기록 (Action 7)

## 의사결정·관리

- [ ] **종합설계서 v1.4 → v1.5 패치**
  - 반영: C1(3차원 확장) C2(전수→시범 재구조화) C3(28+22) C4(LLM Claude Code 병행) — 본 주 결정사항
  - 출력: `04_framework_design/docs/00_프레임워크_종합설계서_v1.md` v1.5 헤더 + 변경 이력
  - 예상 소요: 0.5일

- [ ] **전문가 5인 위촉 메일 초안 + 명단**
  - 구성: 학계 2 + 한국고용정보원 1 + 통계청 (퇴직자) 1 + 산업계 1
  - 출력: `00_project_mgmt/EXPERT_PANEL_위촉.md`
  - 예상 소요: 0.5일

## 다음 주(2026-06-05~) 예고

- Phase 1 명령 1 (`kfw run preprocess`) 실구현
- Phase 1 명령 2 (`kfw run extract-tasks`) 프롬프트 1차 설계 + 단일 KSCO 코드 시험
- 0.6·0.7·0.8 (한국직업사전·O*NET·NCS) 병행 import

---

## 일일 체크 가이드

- 매일 종료 시 본 파일 열고 완료 항목 [x] 처리
- 막힌 항목: 옆에 `BLOCKED: <사유>` 추가, 다음 주 백로그로 이월
- 본 주 마지막 작업일 종료 시 다음 주 백로그 신규 생성 (`WEEKLY_BACKLOG_2026-06-05.md`)
