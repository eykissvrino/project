# 자료_2026-05 — 다운로드 자료 인덱스

작성일: 2026-05-04
출처: O*NET Resource Center, ILO, OECD, Morgeson, SkillTran, 고용노동부, ArXiv 등

---

## 폴더 구조

```
자료_2026-05/
├── A_ONET_공식/           ← O*NET Resource Center 공식 자료 (2024-2026)
├── B_국제프레임워크/       ← ESCO, ISCO-08, SDAIA 등
├── C_한국자료/             ← KECO 2025, KRIVET 보고서
├── D_AI영향연구/           ← ILO/OECD/ArXiv GenAI 영향 분석
├── E_정부인프라/           ← 정부 워크포스 데이터 인프라 사례
├── F_기초자료/             ← Peterson 2001, NRC 2010 등 foundational
├── 이동_스크립트.ps1       ← Downloads → 카테고리 폴더 자동 이동
└── README.md               ← 이 문서
```

## 첫 실행 시 (반드시 1회 필요)

다운로드된 파일들이 **`C:\Users\eykis\Downloads\`** 에 모여 있습니다. 카테고리 폴더로 자동 이동하려면:

```powershell
cd "C:\Users\eykis\OneDrive\vrin_AI_hub\projects\P2026-010_국가데이터처_직업정보 프레임워크 연구\국가데이터처_2026년_직업정보 프레임워크 연구\07_references\자료_2026-05"
.\이동_스크립트.ps1
```

PowerShell 실행 정책 에러 시:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 다운로드된 파일 목록 (2026-05-04 기준)

### A. O*NET 공식 자료 (8개, ~8.8 MB)

| # | 파일명 | 출처 | 발간일 |
|---|--------|------|--------|
| A1 | A1_ONET_2024-08_WorkStyles_Revisiting.pdf | onetcenter.org | 2024-08 |
| A2 | A2_ONET_2025-12_Hybrid_AI_WorkStyle_Ratings.pdf | onetcenter.org | 2025-12 |
| A3 | A3_ONET_2025-12_HigherOrder_WorkStyles.pdf | onetcenter.org | 2025-12 |
| A4 | A4_ONET_2025-10_JobZones_4Level_Framework.pdf | onetcenter.org | 2025-10 |
| A5 | A5_ONET_2025-02_EmergingTasks_RevisedApproach.pdf | onetcenter.org | 2025-02 |
| A6 | A6_ONET_2025-08_AlternateTitles_Automation.pdf | onetcenter.org | 2025-08 |
| A7 | A7_ONET_2026-04_AI_ReferenceTagging.pdf | onetcenter.org | 2026-04 |
| A8 | A8_ONET_2025-05_DroneTasks_ChatGPT.pdf | onetcenter.org | 2025-05 |

### B. 국제 프레임워크 (시도 중)

| # | 파일명 | 출처 | 비고 |
|---|--------|------|------|
| B1 | B1_SDAIA_NationalOccupationalStandard_DataAI.pdf | sdaia.gov.sa | 다운로드 실패 (CORS/지역 제한) |

### C. 한국 자료

| # | 파일명 | 출처 |
|---|--------|------|
| C1 | C1_KECO_2025_kaejeong_hangmokpyo.xlsx | moel.go.kr | KECO 2025 항목표 (다운로드 시도 — 별도 확인 필요) |

### D. AI 영향 연구 (4개, ~12 MB)

| # | 파일명 | 출처 | 발간일 |
|---|--------|------|--------|
| D1 | D1_ILO_2025-05_WP140_GenAI_Jobs_RefinedIndex.pdf | ilo.org | 2025-05 |
| D2 | D2_ArXiv_2025-07_Measuring_Occupational_GenAI_Implications.pdf | arxiv.org | 2025-07 |
| D3 | D3_ArXiv_2025-09_AI_and_Jobs_Review_Theory_Estimates.pdf | arxiv.org | 2025-09 |
| D4 | D4_OECD_2025-11_GenAI_SME_Workforce.pdf | oecd.org | 2025-11 |

### E. 정부·국제기구 인프라 (3개, ~6.8 MB)

| # | 파일명 | 출처 | 발간일 |
|---|--------|------|--------|
| E1 | E1_ILO_2025-01_Digital_Transformation_EmploymentPolicies.pdf | ilo.org | 2025-01 |
| E2 | E2_ILO_Digitalization_Employment_Review.pdf | ilo.org | - |
| E3 | E3_OECD_ILO_EC_2023_Handbook_DigitalPlatform_Employment.pdf | oecd.org | 2023-03 |

### F. 기초 자료 (2개, ~6.5 MB)

| # | 파일명 | 출처 | 발간일 |
|---|--------|------|--------|
| F1 | F1_Peterson_2001_Understanding_Work_ONET.pdf | morgeson.com | 2001 |
| F2 | F2_NRC_2010_Database_Changing_Economy_ONET_Review.pdf | skilltran.com | 2010 |

**합계**: 17~18개 파일, 약 35 MB

---

## 추가 확보 권장 자료 (수동 다운로드 필요)

### 다운로드 어려웠던 자료

1. **KECO 2025 해설서 (KEIS)** — 한국고용정보원 회원 가입 후 다운로드
   - URL: https://www.keis.or.kr/keis/ko/proj/114/pblc/detail.do?pubIdx=11171

2. **ESCO v1.2 데이터 패키지** — ESCO Portal 가입 후 CSV/RDF 다운로드
   - URL: https://esco.ec.europa.eu/en/use-esco/download

3. **Burning Glass Institute *Skills-Based Hiring 2024* 보고서** — 회원가입 또는 메일 등록 필요
   - URL: https://www.burningglassinstitute.org/research/skills-based-hiring-2024

4. ***Skills or degree? The rise of skill-based hiring* (ScienceDirect, 2025)** — 기관 구독 또는 비용 결제 필요
   - URL: https://www.sciencedirect.com/science/article/pii/S0040162525000733

5. **NRC 2010 원본 (NAP)** — 무료지만 양식 작성 필요
   - URL: https://nap.nationalacademies.org/catalog/12814 (현재 skilltran.com 미러본 확보됨)

---

## 다음 단계 권장 작업

1. **PowerShell 스크립트 실행** → 카테고리별 폴더로 정리
2. **A1_WorkStyles_Revisiting** 부터 먼저 한글 요약 (1999 도서 Work Styles 챕터의 현행 후속 자료)
3. **F2_NRC_2010** 9장 *Recommendations* 발췌 → 한국 적용 권고사항 도출
4. **D1_ILO_WP140** 방법론 → 한국 KECO 2025 적용 시뮬레이션 가능성 평가
5. **C1_KECO_2025_항목표** XLSX → 대분류~세분류 구조 파악 후 ESCO/O*NET과 비교표 작성

상세 분석 가이드는 `../최신_ONET_및_관련연구_종합정리_2026-05.md` 참조.
