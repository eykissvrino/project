# Pay Band Simulator — 엑셀 모델 설계서

> 이 문서는 실제 엑셀 파일 개발을 위한 설계도(Spec)입니다.
> `xlsx` 스킬과 결합하여 실제 엑셀 파일 생성.

## 목적
임금구조 설계 시 Pay Band의 Min/Mid/Max, Spread, Overlap을 시뮬레이션하고,
실제 직원 임금 데이터에 적용 시 영향을 즉시 확인.

## 시트 구성

### Sheet 1: README
- 모델 개요
- 시트 안내
- 입력 방법
- 결과 해석 가이드

### Sheet 2: Input — Parameters
| 셀 | 항목 | 입력 예시 |
|----|------|----------|
| B3 | Grade 개수 | 7 |
| B4 | Grade별 Mid 시장 Anchor | (다음 표) |
| B10 | Spread % (각 Grade) | 50% |
| B11 | Overlap % (인접 Grade) | 30% |

#### Grade별 Mid Anchor
| Grade | Mid Anchor (만원) |
|-------|-------------------|
| G1 | 3,000 |
| G2 | 3,800 |
| G3 | 4,800 |
| G4 | 6,200 |
| G5 | 8,000 |
| G6 | 10,500 |
| G7 | 14,000 |

### Sheet 3: Calc — Band 계산
- Min = Mid × (1 - Spread/2 / (1 + Spread/2))
- 또는 Min = Mid / (1 + Spread%/2) 등 룰 명시
- Max = Min × (1 + Spread%)
- Overlap 검증: Grade N Max > Grade N+1 Min?

| Grade | Min | Mid | Max | 이전 Max - 다음 Min (Overlap 검증) |
|-------|-----|-----|-----|-----------------------------------|
| G1 | (수식) | (입력값) | (수식) | - |
| G2 | | | | (수식) |
| ... | | | | |

### Sheet 4: Input — 직원 데이터
| 직원 ID (마스킹) | 현재 직급 | 현재 연봉 | 신 Grade (매핑) |
|-----------------|-----------|----------|---------------|
| EE001 | 과장 | 5,500 | G4 |
| EE002 | 차장 | 7,200 | G5 |
| ... | | | |

### Sheet 5: Calc — 개인별 신임금
| 직원 ID | 현 연봉 | 신 Grade | Grade Min | Grade Max | 신 연봉 (룰) | 변동률 | 분류 |
|---------|---------|----------|-----------|-----------|--------------|--------|------|
| EE001 | 5,500 | G4 | 4,500 | 7,800 | (룰 적용) | +X% | 인상자 |

#### 신 연봉 산정 룰 (옵션 선택)
- **Option A**: 현 연봉 그대로 유지 + Min 미달 시만 Min으로 인상
- **Option B**: 현 연봉을 Band 내 매핑 (Compa-ratio 0.9 권장)
- **Option C**: Performance × Mid

#### 분류 룰
- Min 미달 → **Green Circle** (인상 대상)
- Min ~ Max → **Within Band**
- Max 초과 → **Red Circle** (동결 대상)

### Sheet 6: Output — Dashboard
#### KPI 카드
- 전체 인원
- 인상자 수 / 인상자 비율
- 동결자 수 / 동결자 비율
- 인하자 수 / 인하자 비율
- 평균 변동률
- 인건비 변동 (총액)

#### 차트
- **Histogram**: 변동률 분포 (전체)
- **Box Plot**: Grade별 임금 분포
- **Pay Band 그래프**: Grade별 Min/Mid/Max + 개인 점 분포
- **Scatter**: Compa-ratio 분포

### Sheet 7: Output — Grade별 통계
| Grade | 인원 | 평균 연봉 | Min | Mid | Max | Compa-ratio 평균 |
|-------|------|----------|-----|-----|-----|-----------------|
| G1 | | | | | | |
| G2 | | | | | | |
| ... | | | | | | |

### Sheet 8: Output — 인건비 영향
- 현재 총 인건비
- 신구조 적용 인건비
- 변동 (절대값, %)
- 시나리오: 즉시 vs 단계적 (3년)

## 시각화

### Pay Band 그래프 (가장 중요)
- X축: Grade
- Y축: 연봉
- 막대: Min~Max (Band)
- 점: 개인 (색상으로 분류: 인상자/유지/인하자)

### Compa-ratio Heat Map
- 행: Grade
- 열: 직급 또는 부서
- 색상: Compa-ratio (0.8 빨강 ~ 1.2 녹색)

## 데이터 유효성 (Validation)

- Grade 개수: 3~9 (정수)
- Spread: 20%~80%
- Overlap: 0%~50%
- 직원 데이터: 마스킹 ID 필수

## 사용 시나리오

### 시나리오 1: 신구조 설계 단계
1. Sheet 2에 Grade 수·Spread·Overlap 입력
2. Sheet 4에 직원 데이터 업로드 (마스킹)
3. Sheet 6 Dashboard에서 즉시 영향 확인
4. Spread·Overlap 조정하며 최적안 탐색

### 시나리오 2: 협상·보고
- Sheet 6 Dashboard 인쇄·임원 보고
- "Spread 50% 시 동결자 15%, 인건비 +3%" 식 즉답

## 보안·관리

- 개인식별 정보 마스킹 필수
- Calc 시트 보호 (Password)
- 파일 공유 시 패스워드 설정
- 버전 관리 (v1.0, v1.1 ...)

## 매뉴얼

별도 사용 매뉴얼 (PDF 또는 README 시트):
- 입력 단계별 가이드
- 결과 해석 가이드
- 시나리오 예시
- FAQ
