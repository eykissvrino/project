# 04_framework_design — 한국형 직능유형 프레임워크 설계 (RFP 영역3)

> KSCO 8차 위에 부착하는 한국형 6대 차원 프레임워크 설계.

## 폴더 구조

| 폴더 | 용도 |
|---|---|
| `docs/` | 프레임워크 설계서·차원별 정의·구성요소·측정 척도 |
| `diagrams/` | 6대 차원 도식·계층 구조·데이터 흐름 다이어그램 |

## 한국형 6대 차원 (제안서 차별화 포인트)

| 차원 | 정의 | 모태 |
|---|---|---|
| **업무 (Work Activities)** | 수행되는 주요 업무활동 | O\*NET GWA 41~42 |
| **지식 (Knowledge)** | 이론적·전문적 지식 | O\*NET Knowledge 33 + KSCO 직능유형 ① |
| **기술 (Skills)** | 실무적 기술 | O\*NET Skills 25 |
| **능력 (Abilities)** | 인지·신체적 능력 | O\*NET Abilities 52 |
| **도구 (Tools & Tech)** | 장비·기술·SW | O\*NET Technology + KSCO 직능유형 ② |
| **환경 (Work Context)** | 물리·사회적 환경 | O\*NET Work Context 57 |

## 설계 원칙 (ISCO Companion 모듈 1.3)

- **상호배타성** (Mutually Exclusive)
- **완전성** (Jointly Exhaustive)
- **일관성** (Consistency)
- **국제 비교성** (ISCO-28 정렬)
- **시계열 연속성** (KSCO 7→8차 연결)

## 학술적 정당화 (Peterson 외 2001)

- **Multiple Windows** (다중 관점) — 6차원 동시 기술
- **Common Language** (공통 언어) — 모든 KSCO 세분류 동일 구조
- **Hierarchical Taxonomies** (위계적 분류) — GWA→IWA→DWA→Task

## 산출물 목표

- `한국형_6대차원_프레임워크_설계서.md` (또는 .docx)
- 차원별 구성요소 정의 + 측정 척도 + 활용 시나리오
- 6대 차원 도식 (.svg/.pptx)
- KSCO ↔ KECO 연계 매핑 절차

## 직접 모태 자료

- O\*NET 콘텐츠 모델 2001: [`../01_data_collection/00_external_references/직업정보 관련 참고자료_해외/01_ONET_콘텐츠모델/`](../01_data_collection/00_external_references/직업정보 관련 참고자료_해외/01_ONET_콘텐츠모델/)
- 1995 프로토타입 (4대 원리): [`../01_data_collection/00_external_references/직업정보 관련 참고자료_해외/01_ONET_콘텐츠모델/[1995프로토타입_분석마크다운]_analysis_ONET_prototype_1995.md`](../01_data_collection/00_external_references/직업정보 관련 참고자료_해외/01_ONET_콘텐츠모델/)
- ISCO-08 Companion 모듈 4: [`../01_data_collection/00_external_references/직업정보 관련 참고자료_해외/05_ISCO/`](../01_data_collection/00_external_references/직업정보 관련 참고자료_해외/05_ISCO/)

## 진행 단계

- [ ] M+2 6차원 1차안 (Working Draft)
- [ ] M+3 차원별 구성요소 설계
- [ ] M+4 프레임워크 잠정안 (중간보고)
- [ ] M+7 최종안 확정 (전문가 검토 후)
