# 데이터 분석 스킬

## 용도
설문조사 분석, 직무분석 데이터 처리, HR 애널리틱스, 경영 데이터 분석 등 **컨설팅 프로젝트에서 발생하는 모든 데이터 분석 작업**에 사용합니다.

## 적용 조건
- "데이터 분석해줘", "설문 결과 정리", "통계 분석" 등의 요청
- xlsx, csv 파일의 데이터 처리 및 분석 시
- 차트, 그래프 등 데이터 시각화 시

---

## 분석 유형별 프로세스

### 유형 1: 설문조사 분석

#### 1단계: 데이터 정제
| 작업 | 방법 | 도구 |
|------|------|------|
| 결측치 처리 | 삭제(5% 미만) 또는 대체(평균/중앙값) | pandas `dropna()`, `fillna()` |
| 이상치 탐지 | IQR 방법 (Q1-1.5×IQR ~ Q3+1.5×IQR) | pandas, boxplot |
| 코딩 변환 | 텍스트 응답 → 수치 코드 변환 | pandas `map()`, `replace()` |
| 역코딩 | 부정 문항 역변환 (6-응답값) | pandas 연산 |
| 데이터 검증 | 범위 확인, 논리적 일관성 체크 | 기술통계, 교차검증 |

#### 2단계: 기술통계
```python
import pandas as pd
import numpy as np

# 기본 기술통계
df.describe()                          # 전체 요약
df.groupby('부서').mean()              # 부서별 평균
df.groupby(['부서','직급']).agg(['mean','std','count'])  # 교차 집계
```

| 지표 | 용도 | 해석 기준 |
|------|------|----------|
| 평균(Mean) | 중심 경향 | 리커트 5점: 3.0 미만=부정적, 3.0-3.5=보통, 3.5+=긍정적 |
| 표준편차(SD) | 응답 분산 | SD>1.0이면 의견 분산 큼 → 하위그룹 분석 필요 |
| 빈도(Freq) | 분포 확인 | 최빈값, 특이 분포 확인 |
| 왜도/첨도 | 정규성 | |왜도|>2 또는 |첨도|>7이면 비정규 → 비모수 검정 고려 |

#### 3단계: 교차분석
- **부서별/직급별/연차별** 비교 분석
- 범주형 변수: 카이제곱 검정 (`scipy.stats.chi2_contingency`)
- 연속형 변수: t-검정 (2그룹), ANOVA (3그룹 이상)
- **실무 해석**: 통계적 유의성 + 실질적 차이 크기 함께 보고

#### 4단계: 신뢰도 분석
```python
# Cronbach's Alpha 계산
def cronbachs_alpha(df):
    items = df.shape[1]
    variances = df.var(axis=0, ddof=1)
    total_var = df.sum(axis=1).var(ddof=1)
    return (items / (items - 1)) * (1 - variances.sum() / total_var)
```

| Alpha 값 | 해석 | 조치 |
|----------|------|------|
| 0.9 이상 | 매우 우수 | 유지 |
| 0.8-0.9 | 우수 | 유지 |
| 0.7-0.8 | 양호 | 수용 가능 |
| 0.6-0.7 | 의문 | 문항 검토 필요 |
| 0.6 미만 | 불량 | 문항 재설계 필요 |

### 유형 2: 직무분석 데이터

#### FID 분석 (빈도-중요도-난이도)
```python
# Task 우선순위 산출
df['priority'] = df['frequency'] * df['importance']
df['training_need'] = df['importance'] * df['difficulty']

# 상위 우선순위 Task 추출
top_tasks = df.nlargest(10, 'priority')
```

#### 역량 Gap 분석
```python
# 현재 수준 vs 요구 수준 Gap
df['gap'] = df['required_level'] - df['current_level']
df['gap_ratio'] = df['gap'] / df['required_level'] * 100

# Gap이 큰 순으로 정렬 → 교육 우선순위
priority_competencies = df.nlargest(10, 'gap')
```

### 유형 3: HR 데이터 분석

| 분석 항목 | 지표 | 시각화 |
|----------|------|--------|
| 인력 현황 | 인원수, 평균연령, 성비, 학력분포 | 막대차트, 원형차트 |
| 이직률 | 월별/연별 이직률, 부서별 비교 | 추이 그래프, 히트맵 |
| 근속 | 평균 근속년수, 분포 | 히스토그램 |
| 교육훈련 | 인당 교육시간, 만족도, 과정별 효과 | 막대차트 |
| 성과분포 | 평가등급 분포, 부서별 비교 | 분포도, 박스플롯 |

---

## 시각화 가이드

### 차트 유형 선택
| 데이터 성격 | 권장 차트 | Python 코드 |
|------------|----------|------------|
| 비율/구성 | 원형, 도넛 | `plt.pie()` |
| 비교 | 막대 (가로 권장) | `plt.barh()` |
| 추이/변화 | 꺾은선 | `plt.plot()` |
| 분포 | 히스토그램, 박스플롯 | `plt.hist()`, `plt.boxplot()` |
| 상관관계 | 산점도, 히트맵 | `plt.scatter()`, `sns.heatmap()` |
| 2축 비교 | 버블차트 | `plt.scatter(s=...)` |
| 다변량 비교 | 레이더 차트 | `plt.subplot(polar=True)` |

### 시각화 스타일 표준
```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# 컨설팅 보고서 스타일
COLORS = ['#2C3E50', '#E74C3C', '#3498DB', '#F39C12', '#27AE60']
sns.set_palette(COLORS)
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
```

### 차트 필수 요소
- **제목**: 차트 상단, 볼드, "무엇을 보여주는가" 명확히
- **축 레이블**: 단위 포함 (예: "만족도 (5점 척도)")
- **범례**: 항목 3개 이상일 때 필수
- **출처**: 차트 하단 "출처: OO 설문조사 결과 (N=120)"
- **데이터 레이블**: 핵심 수치는 차트 위에 직접 표기

---

## Excel 분석 가이드

### 피벗테이블 활용
- 부서별/직급별/연차별 교차 집계에 최적
- 행: 분석 대상 (부서, 직급), 열: 비교 항목, 값: 평균/합계/개수

### 조건부서식
- 상위/하위 10% 강조 (빨강/초록)
- 데이터 막대: 수치 크기 시각적 비교
- 아이콘 집합: 달성도 표시 (●◉○)

### 주요 함수
| 용도 | 함수 | 예시 |
|------|------|------|
| 조건부 평균 | `AVERAGEIFS` | 부서별 만족도 평균 |
| 조건부 개수 | `COUNTIFS` | 등급별 인원수 |
| 순위 | `RANK.EQ` | 부서별 성과 순위 |
| 백분율 | `PERCENTILE` | 점수 분위수 |
| 표준편차 | `STDEV.S` | 응답 분산 |

---

## 산출물 형식

| 산출물 | 형식 | 내용 |
|--------|------|------|
| 분석 데이터 | xlsx | 원시데이터 + 정제데이터 + 분석시트 + 요약 |
| 시각화 보고자료 | pptx | 차트 중심 발표 자료 |
| 분석 코드 | .py | 재현 가능한 분석 스크립트 |
| 분석 보고서 | docx | 분석 방법, 결과, 해석 상세 |

### xlsx 시트 구성 표준
```
Sheet 1: 원시데이터 (Raw Data)
Sheet 2: 정제데이터 (Cleaned Data) 
Sheet 3: 기술통계 (Descriptive Statistics)
Sheet 4: 교차분석 (Cross Analysis)
Sheet 5: 차트데이터 (Chart Data)
Sheet 6: 요약 (Executive Summary)
```

---

## 주의사항
- 개인정보가 포함된 원시데이터는 **비식별화** 처리 후 분석
- 통계적 유의성(p<0.05)과 **실질적 의미**를 구분하여 보고
- 표본 크기(N)는 항상 명시 — N<30이면 비모수 검정 사용
- 분석 결과와 해석을 명확히 구분 — 데이터가 말하는 것 vs 컨설턴트의 해석
- 모든 분석은 **재현 가능**하도록 코드 또는 절차 기록
- pptx/docx/xlsx 산출물 작성 시 해당 스킬 연계 사용
