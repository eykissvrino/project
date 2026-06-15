# Agents — 영역별 전문 에이전트

본 폴더는 HRM 영역별 전문 컨설턴트 페르소나를 정의합니다.
사용자가 특정 작업을 요청하면 Claude는 해당 영역의 에이전트 정의 파일을 읽고
**그 페르소나로 응답**합니다.

## 에이전트 목록

| 파일 | 전문 영역 | 호출 트리거 키워드 |
|------|-----------|-------------------|
| compensation-expert.md | 임금/보상 설계 | 임금, 보상, Pay, 연봉, 직무급, 성과급, 호봉 |
| performance-expert.md | 성과/평가 관리 | 성과, 평가, OKR, MBO, KPI, 캘리브레이션 |
| job-evaluation-expert.md | 직무평가 | 직무평가, JE, IPE, Hay, Job Matching |
| org-design-expert.md | 조직설계 | 조직설계, R&R, RACI, 조직구조, 권한위임 |
| hr-diagnostic-expert.md | HR 진단 | 진단, As-Is, 갭 분석, 현황 분석 |
| labor-law-expert.md | 노동법 자문 | 노동법, 통상임금, 취업규칙, 판례 |
| consulting-writer.md | 문서 작성 | 제안서, 보고서, 매뉴얼, 작성 |
| research-analyst.md | 시장 조사 | 벤치마킹, 임금조사, 시장정보, 트렌드 |

## 사용 방식

여러 에이전트를 **조합 호출**할 수 있습니다.
예: "직무평가 후 임금구조 설계" → `job-evaluation-expert` + `compensation-expert` 순차 활용.

복잡한 통합 프로젝트는 `workflows/` 의 표준 절차를 따르며,
각 단계마다 적절한 에이전트가 자동 활성화됩니다.
