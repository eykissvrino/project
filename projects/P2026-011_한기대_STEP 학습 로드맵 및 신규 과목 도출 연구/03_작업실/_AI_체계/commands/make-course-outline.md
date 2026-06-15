---
command: /make-course-outline
description: 과목개요서 1건 작성 (스킬 course-outline-generation 활용)
agents: [course-spec-writer, qa-reviewer]
---

# /make-course-outline

## 인자
- 능력단위 코드 (필수)
- 분야 구분 (평생/디지털/AIX/GX/안전)
- 유형 (E/V/E·V)
- 회차 수 (기본 12)

## 단계

1. 능력단위 정보 조회 (Master DB)
2. 템플릿 로드 (`_AI_체계/templates/과목개요서_{분야}.md`)
3. course-spec-writer가 양식 채움
4. AX 분야이면 `ax-curriculum-expert` 협력
5. qa-reviewer 검수
6. 저장: `03_수행/M5_과목개요서/{분야폴더}/[분야약자]_[세분류]_[과목명].docx`
7. Master DB의 `course_outlines_index` 시트에 등록

## 출력 후 체크
- 양식 100% 채움
- 학습목표 행동 동사
- 참고자료 2024년 이후
- 회차별 능력단위요소 명시
