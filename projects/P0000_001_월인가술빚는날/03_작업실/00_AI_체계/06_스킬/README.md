# 🛠 월인가 자체 스킬 카탈로그

> **스킬은 "어떤 작업을 어떻게 할지"의 모범 사례 묶음.**
> 호출 시 AI가 SKILL.md를 먼저 읽고 그 절차를 따른다.

---

## 1. 스킬 사용법

### 호출
```
@wolinga:brand-voice 이 인스타 캡션 점검해줘
@wolinga:product-card 신제품 약주 상세페이지 만들어줘
```

또는 자연어로 호출:
```
이 캡션 브랜드 보이스에 맞는지 봐줘  → 자동으로 wolinga:brand-voice 적용
```

### 우선 적용
- 콘텐츠 작성 시 **`wolinga:brand-voice` 자동 강제** (콘텐츠 디렉터 호출 시 항상)
- 신제품 등장 시 **`wolinga:product-card` 자동 트리거**

---

## 2. 현재 카탈로그

| 스킬 ID | 상태 | 용도 |
|---------|------|------|
| `wolinga:brand-voice` | ✅ v1 | 브랜드 보이스 강제·점검 |
| `wolinga:product-card` | 🔜 다음 | 신제품 출시용 카드(상세·SNS·라벨) |
| `wolinga:cheonan-pairing` | 🔜 다음 | 천안 자산 페어링 스토리텔링 |
| `wolinga:liquor-license-manager` | 📅 P1 후반 | 주류면허 갱신·변경 워크플로 |
| `wolinga:liquor-tax-helper` | 📅 P1 후반 | 주세 신고 가이드 |
| `wolinga:fermentation-tracker` | 📅 P2 | 발효 일지 입력→분석 |
| `wolinga:tasting-room-host` | 📅 P2 | 시음회·양조장 투어 운영 |
| `wolinga:gov-program-radar` | 📅 P2 | 정부지원사업 발굴·신청서 초안 |
| `wolinga:traditional-d2c-ops` | 📅 P2 | 스마트스토어·전통주 채널 통합 |

---

## 3. 새 스킬 추가 절차

1. `06_스킬/{스킬ID}/` 폴더 생성
2. `SKILL.md` 작성 (메타·목적·트리거·입출력·절차·체크리스트)
3. 본 README의 카탈로그 표 갱신
4. 관련 AI 동료 정의서에 "참조 스킬"로 등록
